<!-- view field -->

<div @include('crud::inc.field_wrapper_attributes') >
  @include($field['view'], ['crud' => $crud, 'entry' => $entry ?? null, 'field' => $field])
</div>
