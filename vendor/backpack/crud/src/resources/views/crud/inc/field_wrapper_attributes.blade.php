<?php
// if the field is required in the FormRequest, it should have an asterisk
$required = (isset($action) && $crud->isRequired($field['name'], $action)) ? ' required' : '';
// if the developer has intentionally set the required attribute on the field
// forget whatever is in the FormRequest, do what the developer wants
$required = (isset($field['showAsterisk'])) ? ($field['showAsterisk'] ? ' required' : '') : $required;
?>

@if (isset($field['wrapperAttributes']))
    @if (!isset($field['wrapperAttributes']['class']))
        class="form-group col-sm-12 {{ $required }}"
    @else
        class="{{ $field['wrapperAttributes']['class'] }} {{ $required }}"
    @endif

    @php
        unset($field['wrapperAttributes']['class']);
    @endphp

    @foreach ($field['wrapperAttributes'] as $attribute => $value)
        @if (is_string($attribute))
            {{ $attribute }}="{{ $value }}"
        @endif
    @endforeach
@else
    class="form-group col-sm-12{{ $required }}"
@endif
