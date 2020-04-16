<?php

namespace Backpack\CRUD\app\Library\CrudPanel\Traits;

trait FakeColumns
{
    /**
     * Returns an array of database columns names, that are used to store fake values or ['extras']
     * if no columns have been found.
     *
     * @return array The fake columns array.
     */
    public function getFakeColumnsAsArray()
    {
        $fakeFieldsColumnsArray = [];

        // get the right fields according to the form type (create/update)
        $fields = $this->getFields();

        foreach ($fields as $field) {
            // if it's a fake field
            if (isset($field['fake']) && $field['fake'] == true) {
                // add it to the request in its appropriate variable - the one defined, if defined
                if (isset($field['store_in'])) {
                    if (! in_array($field['store_in'], $fakeFieldsColumnsArray, true)) {
                        array_push($fakeFieldsColumnsArray, $field['store_in']);
                    }
                } else {
                    //otherwise in the one defined in the $crud variable
                    if (! in_array('extras', $fakeFieldsColumnsArray, true)) {
                        array_push($fakeFieldsColumnsArray, 'extras');
                    }
                }
            }
        }

        if (! count($fakeFieldsColumnsArray)) {
            $fakeFieldsColumnsArray = ['extras'];
        }

        return $fakeFieldsColumnsArray;
    }
}
