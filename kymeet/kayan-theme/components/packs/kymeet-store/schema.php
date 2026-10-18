<?php
defined( 'ABSPATH' ) || exit;

/**
 * KYMEET — Schema نظيف للرئيسية (Organization + Store) بدون مراجعات وهمية.
 */
add_filter( 'rank_math/json_ld', 'kymeet_store_filter_rank_math_json_ld', 999, 2 );
function kymeet_store_filter_rank_math_json_ld( $data, $jsonld ) { // phpcs:ignore
	if ( ! kymeet_store_active() || ! is_front_page() ) {
		return $data;
	}
	return array(
		'@context' => 'https://schema.org',
		'@graph'   => kymeet_store_home_schema_graph(),
	);
}

add_action( 'wp_head', 'kymeet_store_home_schema_print', 20 );
function kymeet_store_home_schema_print() {
	if ( ! kymeet_store_active() || ! is_front_page() ) {
		return;
	}
	if ( function_exists( 'kayan_seo_rank_math_plugin_active' ) && kayan_seo_rank_math_plugin_active() && ! ( function_exists( 'kayan_seo_is_disabled' ) && kayan_seo_is_disabled() ) ) {
		return;
	}
	$graph = kymeet_store_home_schema_graph();
	if ( empty( $graph ) ) {
		return;
	}
	echo '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@graph' => $graph ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>';
}

function kymeet_store_home_schema_graph() {
	$site_name = get_bloginfo( 'name' );
	$site_url  = home_url( '/' );
	$logo      = function_exists( 'kymeet_store_logo_url' ) ? kymeet_store_logo_url() : '';
	if ( ! $logo ) {
		$logo = get_site_icon_url( 512 );
	}
	$desc = get_bloginfo( 'description' );
	if ( function_exists( 'kayan_seo_get_rank_math_description' ) ) {
		$rm = kayan_seo_get_rank_math_description();
		if ( $rm ) {
			$desc = $rm;
		}
	}
	$org_id = $site_url . '#organization';
	$store_id = $site_url . '#store';
	return array(
		array(
			'@type'       => 'Organization',
			'@id'         => $org_id,
			'name'        => $site_name,
			'url'         => $site_url,
			'description' => $desc,
			'logo'        => $logo ? array( '@type' => 'ImageObject', 'url' => $logo ) : null,
		),
		array(
			'@type'        => 'Store',
			'@id'          => $store_id,
			'name'         => $site_name,
			'url'          => $site_url,
			'description'  => $desc,
			'priceCurrency'=> function_exists( 'get_woocommerce_currency' ) ? get_woocommerce_currency() : 'EGP',
			'parentOrganization' => array( '@id' => $org_id ),
			'image'        => $logo ? $logo : null,
		),
		array(
			'@type'       => 'WebSite',
			'@id'         => $site_url . '#website',
			'url'         => $site_url,
			'name'        => $site_name,
			'description' => $desc,
			'inLanguage'  => kymeet_store_is_en() ? 'en' : 'ar',
			'publisher'   => array( '@id' => $org_id ),
			'potentialAction' => array(
				'@type'       => 'SearchAction',
				'target'      => $site_url . 'search/{search_term_string}',
				'query-input' => 'required name=search_term_string',
			),
		),
	);
}
