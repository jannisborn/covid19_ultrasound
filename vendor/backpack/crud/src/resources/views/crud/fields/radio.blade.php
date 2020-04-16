<!-- radio -->
@php
    $optionPointer = 0;
    $optionValue = old(square_brackets_to_dots($field['name'])) ?? $field['value'] ?? $field['default'] ?? '';

    // if the class isn't overwritten, use 'radio'
    if (!isset($field['attributes']['class'])) {
        $field['attributes']['class'] = 'radio';
    }
@endphp

<div @include('crud::inc.field_wrapper_attributes') >

    <div>
        <label>{!! $field['label'] !!}</label>
        @include('crud::inc.field_translatable_icon')
    </div>

    @if( isset($field['options']) && $field['options'] = (array)$field['options'] )

        @foreach ($field['options'] as $value => $label )
            @php ($optionPointer++)

            @if( isset($field['inline']) && $field['inline'] )

            <div class="form-check form-check-inline">
                <input  type="radio"
                        class="form-check-input"
                        id="{{$field['name']}}_{{$optionPointer}}"
                        name="{{$field['name']}}"
                        value="{{$value}}"
                        @include('crud::inc.field_attributes')
                        {{$optionValue == $value ? ' checked': ''}}
                        >
                <label class="radio-inline form-check-label font-weight-normal" for="{{$field['name']}}_{{$optionPointer}}">{!! $label !!}</label>
            </div>

            @else

            <div class="form-check">
                <input  type="radio"
                		class="form-check-input"
                		id="{{$field['name']}}_{{$optionPointer}}"
                		name="{{$field['name']}}"
                		value="{{$value}}"
                		@include('crud::inc.field_attributes')
                		{{$optionValue == $value ? ' checked': ''}}>
                <label class="form-check-label font-weight-normal" for="{{$field['name']}}_{{$optionPointer}}">{!! $label !!}</label>
            </div>

            @endif

        @endforeach

    @endif

    {{-- HINT --}}
    @if (isset($field['hint']))
        <p class="help-block">{!! $field['hint'] !!}</p>
    @endif

</div>
