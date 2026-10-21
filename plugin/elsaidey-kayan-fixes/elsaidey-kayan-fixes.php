<?php
/**
 * Plugin Name: Elsaidey KAYAN Fixes
 * Description: Services CPT archive fix + SEO gap-fill/dedupe for KAYAN/Rank Math (no DB writes).
 * Version: 1.1.0
 * Author: Cursor Agent
 * License: GPL-2.0-or-later
 * Requires PHP: 8.0
 */

if (! defined('ABSPATH')) {
    exit;
}

if (! defined('ELSAIDEY_KAYAN_FIX_ENABLE_SERVICES')) {
    define('ELSAIDEY_KAYAN_FIX_ENABLE_SERVICES', true);
}

if (! defined('ELSAIDEY_KAYAN_FIX_ENABLE_SEO')) {
    define('ELSAIDEY_KAYAN_FIX_ENABLE_SEO', true);
}

final class Elsaidey_Kayan_Fixes {
    private const LEGACY_MARKERS = ['مصور', 'MORSY', 'MOHAMED MORSY', 'فوتوغرافي'];

    private const FALLBACK_HOME_TITLE = 'مؤسسة الصعيدي للمحاماة والاستشارات القانونية | طلخا والمنصورة';
    private const FALLBACK_HOME_DESC  = 'مكتب محاماة في طلخa والمنصورة: استشارات قانونية، جنائي، أسرة، مدني وتجاري. المستشار عيد الصعيدي — اتصل أو راسلنا على واتساب.';

    public static function boot(): void {
        if (ELSAIDEY_KAYAN_FIX_ENABLE_SERVICES) {
            add_action('template_redirect', [self::class, 'render_services_archive'], 9);
        }
        if (ELSAIDEY_KAYAN_FIX_ENABLE_SEO) {
            add_action('template_redirect', [self::class, 'start_html_buffer'], 1);
        }
    }

    public static function start_html_buffer(): void {
        if (is_admin() || wp_doing_ajax() || wp_doing_cron() || (defined('REST_REQUEST') && REST_REQUEST)) {
            return;
        }
        if (is_feed()) {
            return;
        }
        ob_start([self::class, 'process_html']);
    }

    /**
     * Post-process full HTML: dedupe SEO tags; inject only when missing (never call KAYAN output functions).
     */
    public static function process_html(string $html): string {
        if ($html === '' || stripos($html, '<html') === false) {
            return $html;
        }

        $html = self::dedupe_head_tags($html, 'title', '/<title\b[^>]*>.*?<\/title>/is');
        $html = self::dedupe_head_tags($html, 'meta-description', '/<meta\s[^>]*name\s*=\s*["\']description["\'][^>]*>/is');
        $html = self::dedupe_head_tags($html, 'canonical', '/<link\s[^>]*rel\s*=\s*["\']canonical["\'][^>]*>/is');

        $title   = self::resolve_title_string();
        $desc    = self::resolve_description_string();
        $canonical = self::resolve_canonical_url();

        if (! preg_match('/<title\b[^>]*>.*?<\/title>/is', $html) && $title !== '') {
            $inject = '<title>' . esc_html($title) . '</title>' . "\n";
            $html   = preg_replace('/<head(\s[^>]*)?>/i', '<head$1>' . "\n" . $inject, $html, 1);
        }

        if (! preg_match('/<meta\s[^>]*name\s*=\s*["\']description["\']/i', $html) && $desc !== '') {
            $inject = '<meta name="description" content="' . esc_attr($desc) . '" />' . "\n";
            $html   = preg_replace('/<head(\s[^>]*)?>/i', '<head$1>' . "\n" . $inject, $html, 1);
        }

        if ($canonical !== '' && ! preg_match('/<link\s[^>]*rel\s*=\s*["\']canonical["\']/i', $html)) {
            $inject = '<link rel="canonical" href="' . esc_url($canonical) . '" />' . "\n";
            $html   = preg_replace('/<head(\s[^>]*)?>/i', '<head$1>' . "\n" . $inject, $html, 1);
        }

        return $html;
    }

    private static function dedupe_head_tags(string $html, string $label, string $pattern): string {
        if (! preg_match_all($pattern, $html, $matches, PREG_OFFSET_CAPTURE)) {
            return $html;
        }
        if (count($matches[0]) <= 1) {
            return $html;
        }
        $parts = $matches[0];
        for ($i = count($parts) - 1; $i >= 1; $i--) {
            $chunk = $parts[$i][0];
            $html  = str_replace($chunk, '', $html);
        }
        return $html;
    }

    private static function is_legacy_seo_text(string $text): bool {
        foreach (self::LEGACY_MARKERS as $marker) {
            if ($marker !== '' && stripos($text, $marker) !== false) {
                return true;
            }
        }
        return false;
    }

    private static function resolve_title_string(): string {
        if (function_exists('kayan_seo_get_document_title')) {
            $t = wp_strip_all_tags((string) kayan_seo_get_document_title());
            if ($t !== '' && ! self::is_legacy_seo_text($t)) {
                return $t;
            }
        }
        if (function_exists('kayan_seo_get_title')) {
            $t = wp_strip_all_tags((string) kayan_seo_get_title());
            if ($t !== '' && ! self::is_legacy_seo_text($t)) {
                return $t;
            }
        }

        if (is_front_page() || (is_home() && get_option('show_on_front') === 'posts')) {
            $opts = get_option('rank-math-options-titles');
            if (is_array($opts) && ! empty($opts['homepage_title'])) {
                $t = wp_strip_all_tags((string) $opts['homepage_title']);
                if ($t !== '' && ! self::is_legacy_seo_text($t)) {
                    return $t;
                }
            }
            return self::FALLBACK_HOME_TITLE;
        }

        if (is_post_type_archive('services')) {
            $pt = get_post_type_object('services');
            if ($pt && ! empty($pt->labels->name)) {
                $name = wp_strip_all_tags($pt->labels->name);
                $site = function_exists('kayan_seo_get_site_name') ? kayan_seo_get_site_name() : get_bloginfo('name');
                if ($site && stripos($name, $site) === false) {
                    return $name . ' | ' . wp_strip_all_tags($site);
                }
                return $name;
            }
            return 'الخدمات';
        }

        if (is_singular()) {
            return wp_strip_all_tags(get_the_title());
        }

        if (is_category() || is_tag() || is_tax()) {
            $obj = get_queried_object();
            if ($obj && ! empty($obj->name)) {
                return wp_strip_all_tags($obj->name);
            }
        }

        return wp_strip_all_tags(get_bloginfo('name'));
    }

    private static function resolve_description_string(): string {
        if (function_exists('kayan_seo_get_description')) {
            $d = wp_strip_all_tags((string) kayan_seo_get_description());
            if ($d !== '' && ! self::is_legacy_seo_text($d)) {
                return $d;
            }
        }

        if (is_front_page() || (is_home() && get_option('show_on_front') === 'posts')) {
            $opts = get_option('rank-math-options-titles');
            if (is_array($opts) && ! empty($opts['homepage_description'])) {
                $d = wp_strip_all_tags((string) $opts['homepage_description']);
                if ($d !== '' && ! self::is_legacy_seo_text($d)) {
                    return $d;
                }
            }
            return self::FALLBACK_HOME_DESC;
        }

        if (is_post_type_archive('services')) {
            $pt = get_post_type_object('services');
            if ($pt && ! empty($pt->description)) {
                return wp_strip_all_tags($pt->description);
            }
            return 'استعرض خدمات مؤسسة الصعيدي للمحاماة والاستشارات القانونية المنشورة.';
        }

        if (is_singular()) {
            $excerpt = get_the_excerpt();
            if ($excerpt) {
                return wp_strip_all_tags($excerpt);
            }
        }

        $tagline = get_bloginfo('description');
        if ($tagline && ! self::is_legacy_seo_text($tagline)) {
            return wp_strip_all_tags($tagline);
        }

        return '';
    }

    private static function resolve_canonical_url(): string {
        if (function_exists('kayan_seo_get_canonical_url')) {
            $u = (string) kayan_seo_get_canonical_url();
            if ($u !== '') {
                return $u;
            }
        }
        if (is_singular()) {
            return (string) get_permalink();
        }
        if (is_front_page()) {
            return home_url('/');
        }
        if (is_post_type_archive('services')) {
            $link = get_post_type_archive_link('services');
            return $link ? (string) $link : '';
        }
        if (is_category() || is_tag() || is_tax()) {
            $link = get_term_link(get_queried_object());
            return is_wp_error($link) ? '' : (string) $link;
        }
        return '';
    }

    public static function render_services_archive(): void {
        if (is_admin() || wp_doing_ajax() || wp_doing_cron()) {
            return;
        }
        if (! is_post_type_archive('services')) {
            return;
        }
        if (! class_exists('ThemeStatic')) {
            return;
        }

        global $ThemeStatic;
        if (! ($ThemeStatic instanceof ThemeStatic)) {
            return;
        }
        $theme = $ThemeStatic;

        $styles = [
            'kayan-home'  => 'kayan-home.css',
            'kayan-inner' => 'kayan-inner.css',
            'shortcodes'  => 'shortcodes.css',
        ];

        $pt_obj = get_post_type_object('services');
        $title  = $pt_obj && ! empty($pt_obj->labels->name) ? $pt_obj->labels->name : 'الخدمات';
        $sub    = $pt_obj && ! empty($pt_obj->description) ? wp_strip_all_tags($pt_obj->description) : 'جميع خدمات المؤسسة القانونية المنشورة.';

        $theme->Part('header', ['Styles' => $styles]);

        echo '<div class="kayan-inner-archive-shell kayan-tax-archive">';

        if (function_exists('kayan_homepage_render_inner_hero')) {
            kayan_homepage_render_inner_hero(
                [
                    'title'    => $title,
                    'subtitle' => $sub,
                ]
            );
        } else {
            echo '<section class="kayan-inner-hero"><div class="kayan-inner-hero__content">';
            echo '<h1 class="kayan-inner-hero__title">' . esc_html($title) . '</h1>';
            if ($sub !== '') {
                echo '<p class="kayan-inner-hero__sub">' . esc_html($sub) . '</p>';
            }
            echo '</div></section>';
        }

        if (function_exists('kayan_homepage_render_inner_breadcrumb')) {
            kayan_homepage_render_inner_breadcrumb();
        } elseif (function_exists('Breadcrumb')) {
            echo '<div class="kayan-inner-breadcrumb"><div class="kayan-inner-breadcrumb__inner"><div class="YC-BreadCrumb">';
            Breadcrumb();
            echo '</div></div></div>';
        }

        echo '<div class="kayan-inner-body"><div class="kayan-inner-layout kayan-inner-layout--no-sidebar">';
        echo '<section class="kayan-inner-section"><div class="kayan-inner-archive-grid -archivePage-Posts-Grid">';

        $theme->Part(
            'Posts',
            [
                'object__type'      => 'posts',
                'object__name'      => 'services',
                'part_object__name' => 'services',
                'part__name'        => 'Post-box',
                'ScrollLoader'      => true,
                'per'               => 12,
                'show__empty_part'  => 'object--empty',
                'data__empty_part'  => [
                    '__empty_icon'        => '<i class="fa-solid fa-ban"></i>',
                    '__empty_title'       => 'لا توجد خدمات منشورة',
                    '__empty_description' => '<a href="' . esc_url(home_url('/')) . '">الرئيسية</a>',
                ],
            ]
        );

        echo '</div></section></div></div></div>';

        $theme->Part('footer', ['Styles' => $styles]);
        exit;
    }
}

Elsaidey_Kayan_Fixes::boot();
