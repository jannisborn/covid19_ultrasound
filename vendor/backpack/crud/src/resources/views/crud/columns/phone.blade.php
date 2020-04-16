{{-- telephone link --}}
@php
	$value = data_get($entry, $column['name']);
@endphp
<span><a href="tel:{{ $entry->{$column['name']} }}">{{ str_limit(strip_tags($value), array_key_exists('limit', $column) ? $column['limit'] : 40, "[...]") }}</a></span>
