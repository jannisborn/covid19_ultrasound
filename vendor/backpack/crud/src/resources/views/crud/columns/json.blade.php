@if(is_string($entry->{$column['name']}))
<pre>{{ json_encode(json_decode($entry->{$column['name']}, true), JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) }}</pre>
@else
<pre>{{ json_encode($entry->{$column['name']}, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) }}</pre>
@endif
