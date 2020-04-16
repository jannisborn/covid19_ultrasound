{{-- single relationships (1-1, 1-n) --}}
<span>
    <?php
        $attributes = $crud->getModelAttributeFromRelation($entry, $column['entity'], $column['attribute']);
        if (count($attributes)) {
            echo e(str_limit(strip_tags(implode(', ', $attributes)), array_key_exists('limit', $column) ? $column['limit'] : 40, '[...]'));
        } else {
            echo '-';
        }
    ?>
</span>
