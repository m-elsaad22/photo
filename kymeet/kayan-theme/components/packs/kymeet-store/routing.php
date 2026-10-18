<?php
/**
 * KYMEET — إصلاح مسار صفحة المنتج (404 / قالب YourColor)
 */
defined( 'ABSPATH' ) || exit;

add_action( 'template_redirect', 'kymeet_wc_bootstrap_product_query', 1 );
function kymeet_wc_bootstrap_product_query() {
	if ( ! kymeet_wc_active() || ! kymeet_store_active() || is_admin() ) {
		return;
	}
	if ( ! is_404() ) {
		return;
	}
	global $wp, $wp_query;
	$slug = '';
	if ( ! empty( $wp->query_vars['product'] ) ) {
		$slug = sanitize_title( wp_unslash( $wp->query_vars['product'] ) );
	} elseif ( ! empty( $wp->query_vars['name'] ) && isset( $wp->query_vars['post_type'] ) && 'product' === $wp->query_vars['post_type'] ) {
		$slug = sanitize_title( wp_unslash( $wp->query_vars['name'] ) );
	} elseif ( ! empty( $_SERVER['REQUEST_URI'] ) ) { // phpcs:ignore
		$path = wp_parse_url( esc_url_raw( wp_unslash( $_SERVER['REQUEST_URI'] ) ), PHP_URL_PATH ); // phpcs:ignore
		if ( is_string( $path ) && preg_match( '#/product/([^/]+)/?$#', $path, $m ) ) {
			$slug = sanitize_title( $m[1] );
		}
	}
	if ( ! $slug ) {
		return;
	}
	$post = get_page_by_path( $slug, OBJECT, 'product' );
	if ( ! $post || 'publish' !== $post->post_status ) {
		return;
	}
	$wp_query->posts             = array( $post );
	$wp_query->post              = $post;
	$wp_query->post_count        = 1;
	$wp_query->found_posts       = 1;
	$wp_query->max_num_pages     = 1;
	$wp_query->is_404            = false;
	$wp_query->is_single         = true;
	$wp_query->is_singular       = true;
	$wp_query->is_archive        = false;
	$wp_query->is_home           = false;
	$wp_query->queried_object    = $post;
	$wp_query->queried_object_id = (int) $post->ID;
	$GLOBALS['post']             = $post;
	setup_postdata( $post );
	status_header( 200 );
	nocache_headers();
}

add_action( 'template_redirect', 'kymeet_wc_block_legacy_single_widgets', 2 );
function kymeet_wc_block_legacy_single_widgets() {
	if ( ! kymeet_store_active() || ! is_singular( 'product' ) ) {
		return;
	}
	add_filter( 'option_widgets_single__meta', 'kymeet_store_clean_widget_list' );
}
