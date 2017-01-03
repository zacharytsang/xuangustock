										delete_tags[]:96    taxonomy=category
	static function handle_set_parent( $term_ids, $taxonomy ) {
		$parent_id = $_REQUEST['parent'];

		foreach ( $term_ids as $term_id ) {
			if ( $term_id == $parent_id )
				continue;
							要修改的分类ID   要改分类         父节点ID
			$ret = wp_update_term( $term_id, $taxonomy, array( 'parent' => $parent_id ) );

			if ( is_wp_error( $ret ) )
				return false;
		}

		return true;
	}
