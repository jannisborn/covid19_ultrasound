<?php

namespace Backpack\CRUD\app\Library\CrudPanel\Traits;

trait FakeFields
{
    /**
     * Update the request input array to something that can be passed to the model's create or update function.
     * The resulting array will only include the fields that are stored in the database and their values,
     * plus the '_token' and 'redirect_after_save' variables.
     *
     * @param array    $requestInput The request input.
     * @param string   $form         The CRUD form. Can be 'create' or 'update' . Default is 'create'.
     * @param int|bool $id           The CRUD entry id in the case of the 'update' form.
     *
     * @see \Illuminate\Http\Request::all() For an example on how to get the request input.
     *
     * @return array The updated request input.
     */
    public function compactFakeFields($requestInput)
    {
        // get the right fields according to the form type (create/update)
        $fields = $this->fields();

        $compactedFakeFields = [];
        foreach ($fields as $field) {
            // compact fake fields
            // cast the field name to array first, to account for array field names
            // in fields that send multiple inputs and want them all saved to the database
            foreach ((array) $field['name'] as $fieldName) {
                if (isset($field['fake']) && $field['fake'] == true && array_key_exists($fieldName, $requestInput)) {
                    $fakeFieldKey = isset($field['store_in']) ? $field['store_in'] : 'extras';
                    $this->addCompactedField($requestInput, $fieldName, $fakeFieldKey);

                    if (! in_array($fakeFieldKey, $compactedFakeFields)) {
                        $compactedFakeFields[] = $fakeFieldKey;
                    }
                }
            }
        }

        // json_encode all fake_value columns if applicable in the database, so they can be properly stored and interpreted
        foreach ($compactedFakeFields as $value) {
            if (! (property_exists($this->model, 'translatable') && in_array($value, $this->model->getTranslatableAttributes(), true)) && $this->model->shouldEncodeFake($value)) {
                $requestInput[$value] = json_encode($requestInput[$value]);
            }
        }

        // if there are no fake fields defined, return the original request input
        return $requestInput;
    }

    /**
     * Compact a fake field in the request input array.
     *
     * @param array  $requestInput  The request input.
     * @param string $fakeFieldName The fake field name.
     * @param string $fakeFieldKey  The fake field key.
     */
    private function addCompactedField(&$requestInput, $fakeFieldName, $fakeFieldKey)
    {
        $fakeField = $requestInput[$fakeFieldName];
        array_pull($requestInput, $fakeFieldName); // remove the fake field from the request

        $requestInput[$fakeFieldKey][$fakeFieldName] = $fakeField;
    }
}
