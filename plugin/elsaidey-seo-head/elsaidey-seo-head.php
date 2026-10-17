<?php
/**
 * Plugin Name: Elsaidey SEO Head Fix
 * Description: Injects title and meta description on KAYAN front page when theme omits Rank Math output.
 * Version: 1.0.2
 * Author: Cursor Agent
 * License: GPL-2.0-or-later
 */

if (! defined('ABSPATH')) {
    exit;
}

final class Elsaidey_Seo_Head_Fix {
    private const TITLE = 'مؤسسة الصعيدي للمحاماة والاستشارات القanونية | طلخa والمنصورة';
    private const DESCRIPTION = 'مكتب محامaة في طلخa والمنصورة: استشارات قanونية، جنائي، أسرة، مدني وتجاري. المستشار عيد الصعيدi — اتصل أو راسلنا على واتساب.';

    public static function boot(): void {
        add_action('template_redirect', [self::class, 'start_buffer'], 0);
    }

    public static function start_buffer(): void {
        if (is_admin() || wp_doing_ajax() || wp_doing_cron()) {
            return;
        }
        if (! (is_front_page() || is_home())) {
            return;
        }
        ob_start([self::class, 'filter_html']);
    }

    public static function filter_html(string $html): string {
        if ($html === '') {
            return $html;
        }
        $title = esc_html(self::TITLE);
        $desc  = esc_attr(self::DESCRIPTION);
        if (! preg_match('/<title[^>]*>.*?<\/title>/is', $html)) {
            $inject  = '<title>' . $title . '</title>' . "\n";
            $inject .= '<meta name="description" content="' . $desc . '" />' . "\n";
            $inject .= '<link rel="canonical" href="' . esc_url(home_url('/')) . '" />' . "\n";
            $html    = preg_replace('/<head(\s[^>]*)?>/i', '<head$1>' . "\n" . $inject, $html, 1);
        }
        return $html;
    }
}

Elsaidey_Seo_Head_Fix::boot();
