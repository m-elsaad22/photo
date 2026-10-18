<?php
defined( 'ABSPATH' ) || exit;

add_filter( 'body_class', 'kymeet_store_body_classes' );
function kymeet_store_body_classes( $classes ) {
	if ( ! kymeet_store_active() ) {
		return $classes;
	}
	$classes[] = 'kymeet-doc';
	$classes[] = 'kymeet-store-active';
	return $classes;
}

add_action( 'wp_enqueue_scripts', 'kymeet_store_enqueue_assets', 5 );
function kymeet_store_enqueue_assets() {
	if ( ! kymeet_store_active() ) {
		return;
	}
	$base = kymeet_store_url() . 'assets/css/';
	$dir  = kymeet_store_dir() . 'assets/css/';
	$ver  = static function ( $file ) use ( $dir ) {
		$path = $dir . $file;
		return is_readable( $path ) ? (string) filemtime( $path ) : '1';
	};

	wp_enqueue_style( 'kymeet-tokens', $base . 'tokens.css', array(), $ver( 'tokens.css' ) );
	wp_enqueue_style( 'kymeet-fonts', $base . 'fonts.css', array( 'kymeet-tokens' ), $ver( 'fonts.css' ) );
	wp_enqueue_style( 'kymeet-typography', $base . 'typography.css', array( 'kymeet-fonts' ), $ver( 'typography.css' ) );

	$theme_css = get_template_directory() . '/components/styles/kymeet.css';
	if ( is_readable( $theme_css ) ) {
		wp_enqueue_style(
			'kymeet-store-css',
			get_template_directory_uri() . '/components/styles/kymeet.css',
			array( 'kymeet-typography' ),
			(string) filemtime( $theme_css )
		);
	}
}

add_action( 'wp_head', 'kymeet_store_font_preload', 2 );
function kymeet_store_font_preload() {
	if ( ! kymeet_store_active() ) {
		return;
	}
	$fonts = kymeet_store_url() . 'assets/fonts/ibm-plex-sans-arabic/ibm-plex-sans-arabic-400.woff2';
	echo '<link rel="preload" href="' . esc_url( $fonts ) . '" as="font" type="font/woff2" crossorigin>';
}
