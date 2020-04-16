@extends(backpack_view('layouts.top_left'))

@section('before_content_widgets')
	@if (isset($widgets['before_content']))
		@include(backpack_view('inc.widgets'), [ 'widgets' => $widgets['before_content'] ])
	@endif
@endsection

@section('content')
@endsection

@section('after_content_widgets')
	@if (isset($widgets['after_content']))
		@include(backpack_view('inc.widgets'), [ 'widgets' => $widgets['after_content'] ])
	@endif
@endsection