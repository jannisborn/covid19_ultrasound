{{-- Date Range Backpack CRUD filter --}}

<li filter-name="{{ $filter->name }}"
	filter-type="{{ $filter->type }}"
	class="nav-item dropdown {{ Request::get($filter->name)?'active':'' }}">
	<a href="#" class="nav-link dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">{{ $filter->label }} <span class="caret"></span></a>
	<div class="dropdown-menu p-0">
		<div class="form-group backpack-filter mb-0">
			<div class="input-group date">
		        <div class="input-group-prepend">
		          <span class="input-group-text"><i class="fa fa-calendar"></i></span>
		        </div>
		        <input class="form-control pull-right"
		        		id="datepicker-{{ str_slug($filter->name) }}"
		        		type="text"
						@if ($filter->currentValue)
							value="{{ $filter->currentValue }}"
						@endif
		        		>
		        <div class="input-group-append datepicker-{{ str_slug($filter->name) }}-clear-button">
		          <a class="input-group-text" href=""><i class="fa fa-times"></i></a>
		        </div>
		    </div>
		</div>
	</div>
</li>

{{-- ########################################### --}}
{{-- Extra CSS and JS for this particular filter --}}

{{-- FILTERS EXTRA CSS  --}}
{{-- push things in the after_styles section --}}

@push('crud_list_styles')
    <link rel="stylesheet" href="{{ asset('packages/bootstrap-datepicker/dist/css/bootstrap-datepicker3.css') }}">
	<style>
		.input-group.date {
			width: 320px;
			max-width: 100%;
		}
	</style>
@endpush


{{-- FILTERS EXTRA JS --}}
{{-- push things in the after_scripts section --}}

@push('crud_list_scripts')
	<!-- include select2 js-->
	<script src="{{ asset('packages/bootstrap-datepicker/dist/js/bootstrap-datepicker.min.js') }}"></script>
  <script>
		jQuery(document).ready(function($) {
			var dateInput = $('#datepicker-{{ str_slug($filter->name) }}').datepicker({
				autoclose: true,
				format: 'yyyy-mm-dd',
				todayHighlight: true
			})
			.on('changeDate', function(e) {
				var d = new Date(e.date);
				// console.log(e);
				// console.log(d);
				if (isNaN(d.getFullYear())) {
					var value = '';
				} else {
					var value = d.getFullYear() + "-" + ("0"+(d.getMonth()+1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2);
				}

				// console.log(value);

				var parameter = '{{ $filter->name }}';

		    	// behaviour for ajax table
				var ajax_table = $('#crudTable').DataTable();
				var current_url = ajax_table.ajax.url();
				var new_url = addOrUpdateUriParameter(current_url, parameter, value);

				// replace the datatables ajax url with new_url and reload it
				new_url = normalizeAmpersand(new_url.toString());
				ajax_table.ajax.url(new_url).load();

				// add filter to URL
				crud.updateUrl(new_url);

				// mark this filter as active in the navbar-filters
				if (URI(new_url).hasQuery('{{ $filter->name }}', true)) {
					$('li[filter-name={{ $filter->name }}]').removeClass('active').addClass('active');
				}
			});

			$('li[filter-name={{ str_slug($filter->name) }}]').on('filter:clear', function(e) {
				// console.log('date filter cleared');
				$('li[filter-name={{ $filter->name }}]').removeClass('active');
				$('#datepicker-{{ str_slug($filter->name) }}').datepicker('update', '');
				$('#datepicker-{{ str_slug($filter->name) }}').trigger('changeDate');
			});

			// datepicker clear button
			$(".datepicker-{{ str_slug($filter->name) }}-clear-button").click(function(e) {
				e.preventDefault();

				$('li[filter-name={{ str_slug($filter->name) }}]').trigger('filter:clear');
			})
		});
  </script>
@endpush
{{-- End of Extra CSS and JS --}}
{{-- ########################################## --}}