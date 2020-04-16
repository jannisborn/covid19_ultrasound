<!-- select_and_order -->
@php
    $values = isset($field['value']) ? (array)$field['value'] : [];
@endphp

<div @include('crud::inc.field_wrapper_attributes') >
    <label>{!! $field['label'] !!}</label>
    @include('crud::inc.field_translatable_icon')
    <div class="row" 
         data-init-function="bpFieldInitSelectAndOrderElement"
         data-field-name="{{ $field['name'] }}">
        <div class="col-md-12">
        <ul id="{{ $field['name'] }}_selected" data-identifier="selected" class="{{ $field['name'] }}_connectedSortable select_and_order_selected float-left">
            @if(old($field["name"]))
                @if(is_array(old($field["name"])))
                    @foreach (old($field["name"]) as $key)
                        @if(array_key_exists($key,$field['options']))
                            <li value="{{$key}}"><i class="fa fa-arrows"></i> {{ $field['options'][$key] }}</li>
                        @endif
                    @endforeach
                @endif
            @elseif (is_array($values))
                @foreach ($values as $key)
                    @if(array_key_exists($key,$field['options']))
                    <li value="{{$key}}"><i class="fa fa-arrows"></i> {{ $field['options'][$key] }}</li>
                    @endif
                @endforeach
            @endif
        </ul>
        <ul id="{{ $field['name'] }}_all" data-identifier="all" class="{{ $field['name'] }}_connectedSortable select_and_order_all float-right">
            @if(old($field["name"]))
                @foreach ($field['options'] as $key => $value)
                    @if(!is_array(old($field["name"])) || !in_array($key, old($field["name"])))
                        <li value="{{ $key}}"><i class="fa fa-arrows"></i> {{ $value }}</li>
                    @endif
                @endforeach
            @elseif (isset($field['options']))
                @foreach ($field['options'] as $key => $value)
                    @if(is_array($values) && !in_array($key, $values))
                        <li value="{{ $key}}"><i class="fa fa-arrows"></i> {{ $value }}</li>
                    @endif
                @endforeach
            @endif
        </ul>

        {{-- The results will be stored here --}}
        <div id="{{ $field['name'] }}_results">
            @foreach ($values as $key)
                <input type="hidden" name="{{ $field['name'] }}[]" value="{{ $key }}">
            @endforeach
        </div>
    </div>

    {{-- HINT --}}
    @if (isset($field['hint']))
        <p class="help-block">{!! $field['hint'] !!}</p>
    @endif
    </div>
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
    <style>
        .select_and_order_all,
        .select_and_order_selected {
            min-height: 120px;
            list-style-type: none;
            max-height: 220px;
            overflow: scroll;
            overflow-x: hidden;
            padding: 0px 5px 5px 5px;
            border: 1px solid #e6e6e6;
            width: 48%;
        }
        .select_and_order_all {
            border: none;
        }
        .select_and_order_all li,
        .select_and_order_selected li{
            border: 1px solid #eee;
            margin-top: 5px;
            padding: 5px;
            font-size: 1em;
            overflow: hidden;
            cursor: grab;
            border-style: dashed;
        }
        .select_and_order_all li {
            background: #fbfbfb;
            color: grey;
        }
        .select_and_order_selected li {
            border-style: solid;
        }
        .select_and_order_all li.ui-sortable-helper,
        .select_and_order_selected li.ui-sortable-helper {
            color: #3c8dbc;
            border-collapse: #3c8dbc;
            z-index: 9999;
        }
        .select_and_order_all .ui-sortable-placeholder,
        .select_and_order_selected .ui-sortable-placeholder {
            border: 1px dashed #3c8dbc;
            visibility: visible!important;
        }
        .ui-sortable-handle {
            -ms-touch-action: none;
            touch-action: none;
        }

    </style>
    @endpush

    @push('crud_fields_scripts')
        <script src="{{ asset('packages/jquery-ui-dist/jquery-ui.min.js') }}"></script>
    @endpush

@endif

{{-- FIELD JS - will be loaded in the after_scripts section --}}
@push('crud_fields_scripts')
<script>
    function bpFieldInitSelectAndOrderElement(element) {
        var $selected = element.find('[data-identifier=selected]');
        var $all = element.find('[data-identifier=all]');
        var $fieldName = element.attr('data-field-name');

        $( "#"+$fieldName+"_all, #"+$fieldName+"_selected" ).sortable({
            connectWith: "."+$fieldName+"_connectedSortable",
            update: function() {
                var updatedlist = $(this).attr('id');
                if((updatedlist == $fieldName+"_selected")) {
                    $("#"+$fieldName+"_results").html("");
                    if($("#"+$fieldName+"_selected").find('li').length==0) {
                        var input = document.createElement("input");
                        input.setAttribute('name', $fieldName);
                        input.setAttribute('value',null);
                        input.setAttribute('type','hidden');
                        $("#"+$fieldName+"_results").append(input);
                    } else {
                        $("#"+$fieldName+"_selected").find('li').each(function(val,obj) {
                            var input = document.createElement("input");
                            input.setAttribute('name', $fieldName+"[]");
                            input.setAttribute('value',obj.getAttribute('value'));
                            input.setAttribute('type','hidden');
                            $("#"+$fieldName+"_results").append(input);
                        });
                    }
                }
            }
        }).disableSelection();
    }
</script>
@endpush

{{-- End of Extra CSS and JS --}}
{{-- ########################################## --}}
