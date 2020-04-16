@php
	$keyName = isset($column['key']) ? $column['key'] : $column['name'];
	$entryValue = data_get($entry, $keyName);
	$displayValue = isset($column['options'][$entryValue]) ? $column['options'][$entryValue] : '';
@endphp

<span>
	{{ $displayValue }}
</span>