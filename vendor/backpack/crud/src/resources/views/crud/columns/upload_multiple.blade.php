@php
    $value = data_get($entry, $column['name']);
    $prefix = $column['prefix'] ?? '';
@endphp

<span>
    @if ($value && count($value))
        @foreach ($value as $file_path)
            - <a target="_blank" href="{{ isset($column['disk'])?asset(\Storage::disk($column['disk'])->url($file_path)):asset($prefix.$file_path) }}">{{ $prefix.$file_path }}</a><br>
        @endforeach
    @else
        -
    @endif
</span>