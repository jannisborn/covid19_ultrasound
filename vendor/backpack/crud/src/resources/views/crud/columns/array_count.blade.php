{{-- enumerate the values in an array  --}}
@php
    $array = data_get($entry, $column['name']);
@endphp

<span>
    <?php
    $suffix = isset($column['suffix']) ? $column['suffix'] : 'items';

    // the value should be an array wether or not attribute casting is used
    if (! is_array($array)) {
        $array = json_decode($array, true);
    }
    if ($array && count($array)) {
        echo count($array).' '.$suffix;
    } else {
        echo '-';
    }
    ?>
</span>