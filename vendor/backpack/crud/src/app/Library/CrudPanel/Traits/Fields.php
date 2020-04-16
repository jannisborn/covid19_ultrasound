<?php

namespace Backpack\CRUD\app\Library\CrudPanel\Traits;

trait Fields
{
    // ------------
    // FIELDS
    // ------------

    /**
     * Get the CRUD fields for the current operation.
     *
     * @return array
     */
    public function fields()
    {
        return $this->getOperationSetting('fields') ?? [];
    }

    /**
     * Add a field to the create/update form or both.
     *
     * @param string|array $field The new field.
     *
     * @return self
     */
    public function addField($field)
    {
        // if the field_definition_array array is a string, it means the programmer was lazy and has only passed the name
        // set some default values, so the field will still work
        if (is_string($field)) {
            $newField['name'] = $field;
        } else {
            $newField = $field;
        }

        // if this is a relation type field and no corresponding model was specified, get it from the relation method
        // defined in the main model
        if (isset($newField['entity']) && ! isset($newField['model'])) {
            $newField['model'] = $this->getRelationModel($newField['entity']);
        }

        // if the label is missing, we should set it
        if (! isset($newField['label'])) {
            $label = is_array($newField['name']) ? $newField['name'][0] : $newField['name'];
            $newField['label'] = mb_ucfirst(str_replace('_', ' ', $label));
        }

        // if the field type is missing, we should set it
        if (! isset($newField['type'])) {
            $newField['type'] = $this->getFieldTypeFromDbColumnType($newField['name']);
        }

        // if a tab was mentioned, we should enable it
        if (isset($newField['tab'])) {
            if (! $this->tabsEnabled()) {
                $this->enableTabs();
            }
        }

        $fields = $this->getOperationSetting('fields');
        $fieldKey = is_array($newField['name']) ? implode('_', $newField['name']) : $newField['name'];
        $fields = array_add($this->fields(), $fieldKey, $newField);
        $this->setOperationSetting('fields', $fields);

        return $this;
    }

    /**
     * Add multiple fields to the create/update form or both.
     *
     * @param array  $fields The new fields.
     */
    public function addFields($fields)
    {
        if (count($fields)) {
            foreach ($fields as $field) {
                $this->addField($field);
            }
        }
    }

    /**
     * Move the most recently added field after the given target field.
     *
     * @param string $targetFieldName The target field name.
     */
    public function afterField($targetFieldName)
    {
        $this->transformFields(function ($fields) use ($targetFieldName) {
            return $this->moveField($fields, $targetFieldName, false);
        });
    }

    /**
     * Move the most recently added field before the given target field.
     *
     * @param string $targetFieldName The target field name.
     */
    public function beforeField($targetFieldName)
    {
        $this->transformFields(function ($fields) use ($targetFieldName) {
            return $this->moveField($fields, $targetFieldName, true);
        });
    }

    /**
     * Move the most recently added field before or after the given target field. Default is before.
     *
     * @param array  $fields          The form fields.
     * @param string $targetFieldName The target field name.
     * @param bool   $before          If true, the field will be moved before the target field, otherwise it will be moved after it.
     *
     * @return array
     */
    private function moveField($fields, $targetFieldName, $before = true)
    {
        if (array_key_exists($targetFieldName, $fields)) {
            $targetFieldPosition = $before ? array_search($targetFieldName, array_keys($fields))
                : array_search($targetFieldName, array_keys($fields)) + 1;

            if ($targetFieldPosition >= (count($fields) - 1)) {
                // target field name is same as element
                return $fields;
            }

            $element = array_pop($fields);
            $beginningArrayPart = array_slice($fields, 0, $targetFieldPosition, true);
            $endingArrayPart = array_slice($fields, $targetFieldPosition, null, true);

            $fields = array_merge($beginningArrayPart, [$element['name'] => $element], $endingArrayPart);
        }

        return $fields;
    }

    /**
     * Remove a certain field from the create/update/both forms by its name.
     *
     * @param string $name Field name (as defined with the addField() procedure)
     */
    public function removeField($name)
    {
        $this->transformFields(function ($fields) use ($name) {
            array_forget($fields, $name);

            return $fields;
        });
    }

    /**
     * Remove many fields from the create/update/both forms by their name.
     *
     * @param array $array_of_names A simple array of the names of the fields to be removed.
     */
    public function removeFields($array_of_names)
    {
        if (! empty($array_of_names)) {
            foreach ($array_of_names as $name) {
                $this->removeField($name);
            }
        }
    }

    /**
     * Remove all fields from the create/update/both forms.
     */
    public function removeAllFields()
    {
        $current_fields = $this->getCurrentFields();
        if (! empty($current_fields)) {
            foreach ($current_fields as $field) {
                $this->removeField($field['name']);
            }
        }
    }

    /**
     * Update value of a given key for a current field.
     *
     * @param string $field         The field
     * @param array  $modifications An array of changes to be made.
     */
    public function modifyField($field, $modifications)
    {
        $fields = $this->fields();

        foreach ($modifications as $attributeName => $attributeValue) {
            $fields[$field][$attributeName] = $attributeValue;
        }

        $this->setOperationSetting('fields', $fields);
    }

    /**
     * Set label for a specific field.
     *
     * @param string $field
     * @param string $label
     */
    public function setFieldLabel($field, $label)
    {
        $this->modifyField($field, ['label' => $label]);
    }

    /**
     * Check if field is the first of its type in the given fields array.
     * It's used in each field_type.blade.php to determine wether to push the css and js content or not (we only need to push the js and css for a field the first time it's loaded in the form, not any subsequent times).
     *
     * @param array $field The current field being tested if it's the first of its type.
     *
     * @return bool true/false
     */
    public function checkIfFieldIsFirstOfItsType($field)
    {
        $fields_array = $this->getCurrentFields();
        $first_field = $this->getFirstOfItsTypeInArray($field['type'], $fields_array);

        if ($first_field && $field['name'] == $first_field['name']) {
            return true;
        }

        return false;
    }

    /**
     * Decode attributes that are casted as array/object/json in the model.
     * So that they are not json_encoded twice before they are stored in the db
     * (once by Backpack in front-end, once by Laravel Attribute Casting).
     */
    public function decodeJsonCastedAttributes($data)
    {
        $fields = $this->getFields();
        $casted_attributes = $this->model->getCastedAttributes();

        foreach ($fields as $field) {

            // Test the field is castable
            if (isset($field['name']) && is_string($field['name']) && array_key_exists($field['name'], $casted_attributes)) {

                // Handle JSON field types
                $jsonCastables = ['array', 'object', 'json'];
                $fieldCasting = $casted_attributes[$field['name']];

                if (in_array($fieldCasting, $jsonCastables) && isset($data[$field['name']]) && ! empty($data[$field['name']]) && ! is_array($data[$field['name']])) {
                    try {
                        $data[$field['name']] = json_decode($data[$field['name']]);
                    } catch (\Exception $e) {
                        $data[$field['name']] = [];
                    }
                }
            }
        }

        return $data;
    }

    /**
     * @return array
     */
    public function getCurrentFields()
    {
        return $this->fields();
    }

    /**
     * Order the CRUD fields. If certain fields are missing from the given order array, they will be
     * pushed to the new fields array in the original order.
     *
     * @param array $order An array of field names in the desired order.
     */
    public function orderFields($order)
    {
        $this->transformFields(function ($fields) use ($order) {
            return $this->applyOrderToFields($fields, $order);
        });
    }

    /**
     * Apply the given order to the fields and return the new array.
     *
     * @param array $fields The fields array.
     * @param array $order  The desired field order array.
     *
     * @return array The ordered fields array.
     */
    private function applyOrderToFields($fields, $order)
    {
        $orderedFields = [];
        foreach ($order as $fieldName) {
            if (array_key_exists($fieldName, $fields)) {
                $orderedFields[$fieldName] = $fields[$fieldName];
            }
        }

        if (empty($orderedFields)) {
            return $fields;
        }

        $remaining = array_diff_key($fields, $orderedFields);

        return array_merge($orderedFields, $remaining);
    }

    /**
     * Apply the given callback to the form fields.
     *
     * @param callable $callback The callback function to run for the given form fields.
     */
    private function transformFields(callable $callback)
    {
        $this->setOperationSetting('fields', $callback($this->fields()));
    }

    /**
     * Get the fields for the create or update forms.
     *
     * @return array all the fields that need to be shown and their information
     */
    public function getFields()
    {
        return $this->fields();
    }

    /**
     * Check if the create/update form has upload fields.
     * Upload fields are the ones that have "upload" => true defined on them.
     *
     * @param string   $form create/update/both - defaults to 'both'
     * @param bool|int $id   id of the entity - defaults to false
     *
     * @return bool
     */
    public function hasUploadFields()
    {
        $fields = $this->getFields();
        $upload_fields = array_where($fields, function ($value, $key) {
            return isset($value['upload']) && $value['upload'] == true;
        });

        return count($upload_fields) ? true : false;
    }

    // ----------------------
    // FIELD ASSET MANAGEMENT
    // ----------------------

    /**
     * Get all the field types whose resources (JS and CSS) have already been loaded on page.
     *
     * @return array Array with the names of the field types.
     */
    public function getLoadedFieldTypes()
    {
        return $this->getOperationSetting('loadedFieldTypes') ?? [];
    }

    /**
     * Set an array of field type names as already loaded for the current operation.
     *
     * @param array $fieldTypes
     */
    public function setLoadedFieldTypes($fieldTypes)
    {
        $this->setOperationSetting('loadedFieldTypes', $fieldTypes);
    }

    /**
     * Get a namespaced version of the field type name.
     * Appends the 'view_namespace' attribute of the field to the `type', using dot notation.
     *
     * @param  array $field Field array
     * @return string Namespaced version of the field type name. Ex: 'text', 'custom.view.path.text'
     */
    public function getFieldTypeWithNamespace($field)
    {
        $fieldType = $field['type'];

        if (isset($field['view_namespace'])) {
            $fieldType = implode('.', [$field['view_namespace'], $field['type']]);
        }

        return $fieldType;
    }

    /**
     * Add a new field type to the loadedFieldTypes array.
     *
     * @param string $field Field array
     * @return  bool Successful operation true/false.
     */
    public function addLoadedFieldType($field)
    {
        $alreadyLoaded = $this->getLoadedFieldTypes();
        $type = $this->getFieldTypeWithNamespace($field);

        if (! in_array($type, $this->getLoadedFieldTypes(), true)) {
            $alreadyLoaded[] = $type;
            $this->setLoadedFieldTypes($alreadyLoaded);

            return true;
        }

        return false;
    }

    /**
     * Alias of the addLoadedFieldType() method.
     * Adds a new field type to the loadedFieldTypes array.
     *
     * @param string $field Field array
     * @return  bool Successful operation true/false.
     */
    public function markFieldTypeAsLoaded($field)
    {
        return $this->addLoadedFieldType($field);
    }

    /**
     * Check if a field type's reasources (CSS and JS) have already been loaded.
     *
     * @param string $field Field array
     * @return  bool Whether the field type has been marked as loaded.
     */
    public function fieldTypeLoaded($field)
    {
        return in_array($this->getFieldTypeWithNamespace($field), $this->getLoadedFieldTypes());
    }

    /**
     * Check if a field type's reasources (CSS and JS) have NOT been loaded.
     *
     * @param string $field Field array
     * @return  bool Whether the field type has NOT been marked as loaded.
     */
    public function fieldTypeNotLoaded($field)
    {
        return ! in_array($this->getFieldTypeWithNamespace($field), $this->getLoadedFieldTypes());
    }

    /**
     * Get a list of all field names for the current operation.
     *
     * @return array
     */
    public function getAllFieldNames()
    {
        return array_flatten(array_pluck($this->getCurrentFields(), 'name'));
    }

    /**
     * Returns the request without anything that might have been maliciously inserted.
     * Only specific field names that have been introduced with addField() are kept in the request.
     */
    public function getStrippedSaveRequest()
    {
        $setting = $this->getOperationSetting('saveAllInputsExcept');

        if ($setting == false || $setting == null) {
            return $this->request->only($this->getAllFieldNames());
        }

        if (is_array($setting)) {
            return $this->request->except($this->getOperationSetting('saveAllInputsExcept'));
        }

        return $this->request->only($this->getAllFieldNames());
    }
}
