{{-- enumerate the values in an array  --}}
<?php
$array = data_get($entry, $column['name']);

// if the isn't using attribute casting, decode it
if (is_string($array)) {
    $array = json_decode($array);
}

if (is_array($array) && count($array)) {
    $list = [];
    foreach ($array as $item) {
        if (isset($item->{$column['visible_key']})) {
            $list[] = $item->{$column['visible_key']};
        } elseif (is_array($item) && isset($item[$column['visible_key']])) {
            $list[] = $item[$column['visible_key']];
        }
    }
    $displayValue = implode(', ', $list);
}
?>
<span>
    {{ $displayValue ?? '-' }}
</span>