<?php
/**
 * Plugin Name: Elsaidey KAYAN Fixes
 * Description: Fixes /services/ CPT archive fatal error and restores front-end SEO title/meta when KAYAN SEO head output is missing.
 * Version: 1.0.0
 * Author: Cursor Agent
 * License: GPL-2.0-or-later
 * Requires at least: 6.0
 * Requires PHP: 7.4
 */

if (! defined('ABSPATH')) {
    exit;
}

final class Elsaidey_Kayan_Fixes {
    private const RM_HOMEPAGE_TITLE = 'مؤسسة الصعيدي للمحاماة والاستشارات القانونية | طلخا والمنصورة';
    private const RM_HOMEPAGE_DESC  = 'مكتب محاماة في طلخا والمنصورة: استشارات قانونية، جنائي، أسرة، مدني وتجاري. المستشار عيد الصعيدي — اتصل أو راسلنا على واتساب.';

    public static function boot(): void {
        register_activation_hook(__FILE__, [self::class, 'on_activate']);
        add_action('template_redirect', [self::class, 'render_services_archive'], 9);
        add_action('wp_head', [self::class, 'emit_document_seo'], 0);
    }

    public static function on_activate(): void {
        self::maybe_patch_rank_math_homepage();
    }

    private static function maybe_patch_rank_math_homepage(): void {
        $opts = get_option('rank-math-options-titles');
        if (! is_array($opts)) {
            return;
        }
        $changed = false;
        if (empty($opts['homepage_title']) || str_contains((string) $opts['homepage_title'], 'مصور')) {
            $opts['homepage_title'] = self::RM_HOMEPAGE_TITLE;
            $changed                = true;
        }
        if (empty($opts['homepage_description']) || str_contains((string) $opts['homepage_description'], 'مصور')) {
            $opts['homepage_description'] = self::RM_HOMEPAGE_DESC;
            $changed                      = true;
        }
        if (! empty($opts['knowledgegraph_name']) && str_contains((string) $opts['knowledgegraph_name'], 'MORSY')) {
            $opts['knowledgegraph_name'] = 'مؤسسة الصعيدي للمحاماة والاستشارات القانونية';
            $changed                     = true;
        }
        if ($changed) {
            update_option('rank-math-options-titles', $opts);
        }
    }

    /**
     * KAYAN @archive/shape.php falls back to default.php for post-type archives when
     * archive-{post_type}.php is missing; default.php expects WP_Term → fatal on PHP 8.1+.
     */
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
        $theme = ($ThemeStatic instanceof ThemeStatic) ? $ThemeStatic : new ThemeStatic();

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
                'object__type'       => 'posts',
                'object__name'       => 'services',
                'part_object__name'  => 'services',
                'part__name'         => 'Post-box',
                'ScrollLoader'       => true,
                'per'                => 12,
                'show__empty_part'   => 'object--empty',
                'data__empty_part'   => [
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

    /**
     * KAYAN SEO bridge disables Rank Math head output; when theme hooks fail, pages have no title/description.
     * Prefer KAYAN SEO helpers (Rank Math settings as source); no duplicate if already printed.
     */
    public static function emit_document_seo(): void {
        static $done = false;
        if ($done) {
            return;
        }

        $title_html = '';
        $meta_html  = '';

        if (function_exists('kayan_seo_output_document_title_tag')) {
            ob_start();
            kayan_seo_output_document_title_tag();
            $title_html = (string) ob_get_clean();
        }
        if (function_exists('kayan_seo_render_head_meta')) {
            ob_start();
            kayan_seo_render_head_meta();
            $meta_html = (string) ob_get_clean();
        }

        if ($title_html === '' || ! preg_match('/<title\b/i', $title_html)) {
            $title = self::resolve_fallback_title();
            if ($title !== '') {
                $title_html = '<title>' . esc_html($title) . '</title>' . "\n";
            }
        }

        if ($meta_html === '' || ! preg_match('/name=["\']description["\']/i', $meta_html)) {
            $desc = self::resolve_fallback_description();
            if ($desc !== '') {
                $meta_html = '<meta name="description" content="' . esc_attr($desc) . '" />' . "\n";
            }
        }

        if ($title_html !== '') {
            echo $title_html; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
        }
        if ($meta_html !== '') {
            echo $meta_html; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
        }

        $done = true;
    }

    private static function resolve_fallback_title(): string {
        if (function_exists('kayan_seo_get_document_title')) {
            $t = kayan_seo_get_document_title();
            if ($t !== '') {
                return $t;
            }
        }
        if (is_front_page() || (is_home() && get_option('show_on_front') === 'posts')) {
            $opts = get_option('rank-math-options-titles');
            if (is_array($opts) && ! empty($opts['homepage_title'])) {
                return wp_strip_all_tags($opts['homepage_title']);
            }
            return self::RM_HOMEPAGE_TITLE;
        }
        if (is_singular()) {
            return wp_strip_all_tags(get_the_title());
        }
        return wp_strip_all_tags(get_bloginfo('name'));
    }

    private static function resolve_fallback_description(): string {
        if (function_exists('kayan_seo_get_description')) {
            $d = kayan_seo_get_description();
            if ($d !== '') {
                return $d;
            }
        }
        if (is_front_page() || (is_home() && get_option('show_on_front') === 'posts')) {
            $opts = get_option('rank-math-options-titles');
            if (is_array($opts) && ! empty($opts['homepage_description'])) {
                return wp_strip_all_tags($opts['homepage_description']);
            }
            return self::RM_HOMEPAGE_DESC;
        }
        if (is_singular()) {
            $excerpt = get_the_excerpt();
            if ($excerpt) {
                return wp_strip_all_tags($excerpt);
            }
        }
        return wp_strip_all_tags(get_bloginfo('description'));
    }

    private static function current_url(): string {
        if (function_exists('kayan_seo_get_canonical_url')) {
            $u = kayan_seo_get_canonical_url();
            if ($u) {
                return $u;
            }
        }
        global $wp;
        if (isset($wp) && is_object($wp)) {
            return home_url(add_query_arg([], $wp->request));
        }
        return home_url('/');
    }
}

Elsaidey_Kayan_Fixes::boot();
