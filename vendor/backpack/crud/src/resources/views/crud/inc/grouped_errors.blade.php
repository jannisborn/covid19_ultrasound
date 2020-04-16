{{-- Show the errors, if any --}}
@if ($crud->groupedErrorsEnabled() && $errors->any())
    <div class="alert alert-danger pb-0">
        <ul class="list-unstyled">
            @foreach($errors->all() as $error)
                <li><i class="fa fa-info-circle"></i> {{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif