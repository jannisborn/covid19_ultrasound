{{-- relationships with pivot table (n-n) --}}
@php
    $results = data_get($entry, $column['name']);
@endphp

<span>
    <?php
        if ($results && $results->count()) {
            $results_array = $results->pluck($column['attribute']);
            echo implode(', ', $results_array->toArray());
        } else {
            echo '-';
        }
    ?>
</span>