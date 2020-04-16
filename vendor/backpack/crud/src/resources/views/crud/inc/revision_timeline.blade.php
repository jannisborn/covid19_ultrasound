
@foreach($revisions as $revisionDate => $dateRevisions)
      <h5 class="text-primary">
        {{ Carbon\Carbon::parse($revisionDate)->isoFormat(config('backpack.base.default_date_format')) }}
      </h5>

  @foreach($dateRevisions as $history)
    <div class="card">

      @if($history->key == 'created_at' && !$history->old_value)
        <div class="card-header">
          <strong class="time"><i class="fa fa-clock-o"></i> {{ date('h:ia', strtotime($history->created_at)) }}</strong> -
          {{ $history->userResponsible()?$history->userResponsible()->name:trans('backpack::crud.guest_user') }} {{ trans('backpack::crud.created_this') }} {{ $crud->entity_name }}
        </div>
      @else
        <div class="card-header">
          <strong class="time"><i class="fa fa-clock-o"></i> {{ date('h:ia', strtotime($history->created_at)) }}</strong> -
          {{ $history->userResponsible()?$history->userResponsible()->name:trans('backpack::crud.guest_user') }} {{ trans('backpack::crud.changed_the') }} {{ $history->fieldName() }}
          <div class="card-header-actions">
            <form class="card-header-action" method="post" action="{{ url(\Request::url().'/'.$history->id.'/restore') }}">
              {!! csrf_field() !!}
              <button type="submit" class="btn btn-outline-danger btn-sm restore-btn" data-entry-id="{{ $entry->id }}" data-revision-id="{{ $history->id }}" onclick="onRestoreClick(event)">
                <i class="fa fa-undo"></i> {{ trans('backpack::crud.undo') }}</button>
              </form>
          </div>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-6">{{ mb_ucfirst(trans('backpack::crud.from')) }}:</div>
            <div class="col-md-6">{{ mb_ucfirst(trans('backpack::crud.to')) }}:</div>
          </div>
          <div class="row">
            <div class="col-md-6"><div class="alert alert-danger" style="overflow: hidden;">{{ $history->oldValue() }}</div></div>
            <div class="col-md-6"><div class="alert alert-success" style="overflow: hidden;">{{ $history->newValue() }}</div></div>
          </div>
        </div>
      @endif
    </div>
  @endforeach
@endforeach

@section('after_scripts')
  <script type="text/javascript">
    $.ajaxPrefilter(function(options, originalOptions, xhr) {
        var token = $('meta[name="csrf_token"]').attr('content');

        if (token) {
              return xhr.setRequestHeader('X-XSRF-TOKEN', token);
        }
    });
    function onRestoreClick(e) {
      e.preventDefault();
      var entryId = $(e.target).attr('data-entry-id');
      var revisionId = $(e.target).attr('data-revision-id');
      $.ajax('{{ \Request::url().'/' }}' +  revisionId + '/restore', {
        method: 'POST',
        data: {
          revision_id: revisionId
        },
        success: function(revisionTimeline) {
          // Replace the revision list with the updated revision list
          $('.timeline').replaceWith(revisionTimeline);

          // Animate the new revision in (by sliding)
          $('.timeline-item-wrap').first().addClass('fadein');
          new Noty({
              type: "success",
              text: "{{ trans('backpack::crud.revision_restored') }}"
          }).show();
        }
      });
  }
  </script>
@endsection

@section('after_styles')
  {{-- Animations for new revisions after ajax calls --}}
  <style>
     .timeline-item-wrap.fadein {
      -webkit-animation: restore-fade-in 3s;
              animation: restore-fade-in 3s;
    }
    @-webkit-keyframes restore-fade-in {
      from {opacity: 0}
      to {opacity: 1}
    }
      @keyframes restore-fade-in {
        from {opacity: 0}
        to {opacity: 1}
    }
  </style>
@endsection
