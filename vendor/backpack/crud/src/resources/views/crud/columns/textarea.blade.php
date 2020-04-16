{{-- regular object attribute --}}
@php
    $value = data_get($entry, $column['name']);
    $value = is_string($value) ? $value : ''; // don't try to show arrays/object if the column was autoSet
@endphp

<span>{!! $value !!}</span>