<!-- Simple MDE - Markdown Editor -->
<div @include('crud::inc.field_wrapper_attributes') >
    <label>{!! $field['label'] !!}</label>
    @include('crud::inc.field_translatable_icon')
    <textarea
    	id="simplemde_{{ $field['name'] }}"
        name="{{ $field['name'] }}"
        data-init-function="bpFieldInitSimpleMdeElement"
        data-simplemdeAttributesRaw="{{ isset($field['simplemdeAttributesRaw']) ? "{".$field['simplemdeAttributesRaw']."}" : "{}" }}"
        data-simplemdeAttributes="{{ isset($field['simplemdeAttributes']) ? json_encode($field['simplemdeAttributes']) : "{}" }}"
        @include('crud::inc.field_attributes', ['default_class' => 'form-control'])
    	>{{ old(square_brackets_to_dots($field['name'])) ?? $field['value'] ?? $field['default'] ?? '' }}</textarea>

    {{-- HINT --}}
    @if (isset($field['hint']))
        <p class="help-block">{!! $field['hint'] !!}</p>
    @endif
</div>


{{-- ########################################## --}}
{{-- Extra CSS and JS for this particular field --}}
{{-- If a field type is shown multiple times on a form, the CSS and JS will only be loaded once --}}
@if ($crud->fieldTypeNotLoaded($field))
    @php
        $crud->markFieldTypeAsLoaded($field);
    @endphp

    {{-- FIELD CSS - will be loaded in the after_styles section --}}
    @push('crud_fields_styles')
        <link rel="stylesheet" href="{{ asset('packages/simplemde/dist/simplemde.min.css') }}">
        <style type="text/css">
        .CodeMirror-fullscreen, .editor-toolbar.fullscreen {
            z-index: 9999 !important;
        }
        .CodeMirror{
        	min-height: auto !important;
        }
        </style>
    @endpush

    {{-- FIELD JS - will be loaded in the after_scripts section --}}
    @push('crud_fields_scripts')
        <script src="{{ asset('packages/simplemde/dist/simplemde.min.js') }}"></script>
        <script>
            function bpFieldInitSimpleMdeElement(element) {
                var elementId = element.attr('id');
                var simplemdeAttributes = JSON.parse(element.attr('data-simplemdeAttributes'));
                var simplemdeAttributesRaw = JSON.parse(element.attr('data-simplemdeAttributesRaw'));
                var configurationObject = {
                    element: $('#'+elementId)[0],
                };

                configurationObject = Object.assign(configurationObject, simplemdeAttributes, simplemdeAttributesRaw);

                //by default we prevent the loading of fontawesome
                if(!configurationObject.autoDownloadFontAwesome) {
                    configurationObject.autoDownloadFontAwesome = false;
                }

                var smdeObject = new SimpleMDE(configurationObject);

                smdeObject.options.minHeight = smdeObject.options.minHeight || "300px";
                smdeObject.codemirror.getScrollerElement().style.minHeight = smdeObject.options.minHeight;
                $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
                    setTimeout(function() { smdeObject.codemirror.refresh(); }, 10);
                });
            }
        </script>
    @endpush

@endif

{{-- End of Extra CSS and JS --}}
{{-- ########################################## --}}
