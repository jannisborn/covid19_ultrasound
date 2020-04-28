@php
    $value = data_get($entry, $column['name']);
    $prefix = $column['prefix'] ?? '';

    if (is_array($value)) {
      $value = json_encode($value);
    }

    $filePath = Storage::disk($column['disk'])->path($prefix.$value);
    $mime = Storage::disk($column['disk'])->mimeType($prefix.$value);
    $base64 = '';
    if (file_exists($filePath)) {
        $base64 = base64_encode(file_get_contents($filePath));
    }
@endphp

<span>
  @if( empty($base64) )
        File not found
    @else
        <img src="data:{{ $mime }};base64,{{ $base64 }}" style="
            max-height: {{ isset($column['height']) ? $column['height'] : "25px" }};
            width: {{ isset($column['width']) ? $column['width'] : "auto" }};
            border-radius: 3px;"
        />
    @endif
</span>
