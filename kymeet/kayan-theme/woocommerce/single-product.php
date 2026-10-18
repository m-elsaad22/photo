<?php
/**
 * WooCommerce single product — KAYAN ThemeStatic renders @single/product.php.
 * This file satisfies WC template hierarchy when Woo looks for overrides.
 */
defined( 'ABSPATH' ) || exit;

while ( have_posts() ) {
	the_post();
	wc_get_template_part( 'content', 'single-product' );
}
