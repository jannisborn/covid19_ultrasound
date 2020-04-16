<!-- icon picker input -->
@php
    // if no iconset was provided, set the default iconset to Font-Awesome
    $field['iconset'] = $field['iconset'] ?? 'fontawesome';

    switch ($field['iconset']) {
        case 'ionicon':
            $fontIconFilePath = asset('packages/bootstrap-iconpicker/icon-fonts/ionicons-1.5.2/css/ionicons.min.css');
            break;
        case 'weathericon':
            $fontIconFilePath = asset('packages/bootstrap-iconpicker/icon-fonts/weather-icons-1.2.0/css/weather-icons.min.css');
            break;
        case 'mapicon':
            $fontIconFilePath = asset('packages/bootstrap-iconpicker/icon-fonts/map-icons-2.1.0/css/map-icons.min.css');
            break;
        case 'octicon':
            $fontIconFilePath = asset('packages/bootstrap-iconpicker/icon-fonts/octicons-2.1.2/css/octicons.min.css');
            break;
        case 'typicon':
            $fontIconFilePath = asset('packages/bootstrap-iconpicker/icon-fonts/typicons-2.0.6/css/typicons.min.css');
            break;
        case 'elusiveicon':
            $fontIconFilePath = asset('packages/bootstrap-iconpicker/icon-fonts/elusive-icons-2.0.0/css/elusive-icons.min.css');
            break;
        case 'meterialdesign':
            $fontIconFilePath = asset('packages/bootstrap-iconpicker/icon-fonts/material-design-1.1.1/css)/material-design-iconic-font.min.css');
            break;
        default:
            $fontIconFilePath = asset('packages/bootstrap-iconpicker/icon-fonts/font-awesome-5.10.1/css/all.min.css');
            break;
    }

    $fontIconFilePath = $field['font_icon_file_path'] ?? $fontIconFilePath;

@endphp

<div @include('crud::inc.field_wrapper_attributes') >
    <label>{!! $field['label'] !!}</label>
    @include('crud::inc.field_translatable_icon')

    <div>
        <button class="btn btn-light btn-sm" role="iconpicker" data-icon="{{ old(square_brackets_to_dots($field['name'])) ?? $field['value'] ?? $field['default'] ?? '' }}" data-iconset="{{ $field['iconset'] }}"></button>
        <input
            type="hidden"
            name="{{ $field['name'] }}"
            data-init-function="bpFieldInitIconPickerElement"
            value="{{ old(square_brackets_to_dots($field['name'])) ?? $field['value'] ?? $field['default'] ?? '' }}"
            @include('crud::inc.field_attributes')
        >
    </div>

    {{-- HINT --}}
    @if (isset($field['hint']))
        <p class="help-block">{!! $field['hint'] !!}</p>
    @endif
</div>


@if ($crud->fieldTypeNotLoaded($field))
    @php
        $crud->markFieldTypeAsLoaded($field);
    @endphp

    {{-- FIELD EXTRA CSS  --}}
    @push('crud_fields_styles')
        {{-- The chosen font --}}
        <link rel="stylesheet" type="text/css" href="{{ $fontIconFilePath }}">
        <!-- Bootstrap-Iconpicker -->
        <link rel="stylesheet" href="{{ asset('packages/bootstrap-iconpicker/bootstrap-iconpicker/css/bootstrap-iconpicker.min.css') }}"/>
    @endpush

    {{-- FIELD EXTRA JS --}}
    @push('crud_fields_scripts')
        <!-- Bootstrap-Iconpicker -->
        <script type="text/javascript" src="{{ asset('packages/bootstrap-iconpicker/bootstrap-iconpicker/js/bootstrap-iconpicker.bundle.min.js') }}"></script>

        {{-- Bootstrap-Iconpicker - set hidden input value --}}
        <script>
            function bpFieldInitIconPickerElement(element) {
                element.siblings('button[role=iconpicker]').on('change', function(e) {
                    $(this).siblings('input[type=hidden]').val(e.icon);
                });
            }
        </script>
    @endpush

@endif


{{-- Note: you can use @if ($crud->checkIfFieldIsFirstOfItsType($field, $fields)) to only load some CSS/JS once, even though there are multiple instances of it --}}
