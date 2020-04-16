<?php

namespace Backpack\CRUD\app\Library\CrudPanel\Traits;

use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasOne;

trait Create
{
    /*
    |--------------------------------------------------------------------------
    |                                   CREATE
    |--------------------------------------------------------------------------
    */

    /**
     * Insert a row in the database.
     *
     * @param array $data All input values to be inserted.
     *
     * @return \Illuminate\Database\Eloquent\Model
     */
    public function create($data)
    {
        $data = $this->decodeJsonCastedAttributes($data);
        $data = $this->compactFakeFields($data);

        // omit the n-n relationships when updating the eloquent item
        $nn_relationships = array_pluck($this->getRelationFieldsWithPivot(), 'name');
        $item = $this->model->create(array_except($data, $nn_relationships));

        // if there are any relationships available, also sync those
        $this->createRelations($item, $data);

        return $item;
    }

    /**
     * Get all fields needed for the ADD NEW ENTRY form.
     *
     * @return array The fields with attributes and fake attributes.
     */
    public function getCreateFields()
    {
        return $this->fields();
    }

    /**
     * Get all fields with relation set (model key set on field).
     *
     * @return array The fields with model key set.
     */
    public function getRelationFields()
    {
        $fields = $this->fields();
        $relationFields = [];

        foreach ($fields as $field) {
            if (isset($field['model'])) {
                array_push($relationFields, $field);
            }

            if (isset($field['subfields']) &&
                is_array($field['subfields']) &&
                count($field['subfields'])) {
                foreach ($field['subfields'] as $subfield) {
                    array_push($relationFields, $subfield);
                }
            }
        }

        return $relationFields;
    }

    /**
     * Get all fields with n-n relation set (pivot table is true).
     *
     * @return array The fields with n-n relationships.
     */
    public function getRelationFieldsWithPivot()
    {
        $all_relation_fields = $this->getRelationFields();

        return array_where($all_relation_fields, function ($value, $key) {
            return isset($value['pivot']) && $value['pivot'];
        });
    }

    /**
     * Create the relations for the current model.
     *
     * @param \Illuminate\Database\Eloquent\Model $item The current CRUD model.
     * @param array                               $data The form data.
     */
    public function createRelations($item, $data)
    {
        $this->syncPivot($item, $data);
        $this->createOneToOneRelations($item, $data);
    }

    /**
     * Sync the declared many-to-many associations through the pivot field.
     *
     * @param \Illuminate\Database\Eloquent\Model $model The current CRUD model.
     * @param array                               $data  The form data.
     */
    public function syncPivot($model, $data)
    {
        $fields_with_relationships = $this->getRelationFields();

        foreach ($fields_with_relationships as $key => $field) {
            if (isset($field['pivot']) && $field['pivot']) {
                $values = isset($data[$field['name']]) ? $data[$field['name']] : [];

                $relation_data = [];
                foreach ($values as $pivot_id) {
                    $pivot_data = [];

                    if (isset($field['pivotFields'])) {
                        foreach ($field['pivotFields'] as $pivot_field_name) {
                            $pivot_data[$pivot_field_name] = $data[$pivot_field_name][$pivot_id];
                        }
                    }
                    $relation_data[$pivot_id] = $pivot_data;
                }

                $model->{$field['name']}()->sync($relation_data);
            }

            if (isset($field['morph']) && $field['morph'] && isset($data[$field['name']])) {
                $values = $data[$field['name']];
                $model->{$field['name']}()->sync($values);
            }
        }
    }

    /**
     * Create any existing one to one relations for the current model from the form data.
     *
     * @param \Illuminate\Database\Eloquent\Model $item The current CRUD model.
     * @param array                               $data The form data.
     */
    private function createOneToOneRelations($item, $data)
    {
        $relationData = $this->getRelationDataFromFormData($data);
        $this->createRelationsForItem($item, $relationData);
    }

    /**
     * Create any existing one to one relations for the current model from the relation data.
     *
     * @param \Illuminate\Database\Eloquent\Model $item          The current CRUD model.
     * @param array                               $formattedData The form data.
     *
     * @return bool|null
     */
    private function createRelationsForItem($item, $formattedData)
    {
        if (! isset($formattedData['relations'])) {
            return false;
        }

        foreach ($formattedData['relations'] as $relationMethod => $relationData) {
            $model = $relationData['model'];
            $relation = $item->{$relationMethod}();

            if ($relation instanceof BelongsTo) {
                $modelInstance = $model::find($relationData['values'])->first();
                if ($modelInstance != null) {
                    $relation->associate($modelInstance)->save();
                } else {
                    $relation->dissociate()->save();
                }
            } elseif ($relation instanceof HasOne) {
                if ($item->{$relationMethod} != null) {
                    $item->{$relationMethod}->update($relationData['values']);
                    $modelInstance = $item->{$relationMethod};
                } else {
                    $modelInstance = new $model($relationData['values']);
                    $relation->save($modelInstance);
                }
            } else {
                $modelInstance = new $model($relationData['values']);
                $relation->save($modelInstance);
            }

            if (isset($relationData['relations'])) {
                $this->createRelationsForItem($modelInstance, ['relations' => $relationData['relations']]);
            }
        }
    }

    /**
     * Get a relation data array from the form data.
     * For each relation defined in the fields through the entity attribute, set the model, the parent model and the
     * attribute values. For relations defined with the "dot" notations, this will be used to calculate the depth in the
     * final array (@see \Illuminate\Support\Arr::set() for more).
     *
     * @param array $data The form data.
     *
     * @return array The formatted relation data.
     */
    private function getRelationDataFromFormData($data)
    {
        $relationFields = $this->getRelationFields();

        $relationData = [];
        foreach ($relationFields as $relationField) {
            $attributeKey = $relationField['name'];
            if (array_key_exists($attributeKey, $data) && empty($relationField['pivot'])) {
                $key = implode('.relations.', explode('.', $relationField['entity']));
                $fieldData = array_get($relationData, 'relations.'.$key, []);

                if (! array_key_exists('model', $fieldData)) {
                    $fieldData['model'] = $relationField['model'];
                }

                if (! array_key_exists('parent', $fieldData)) {
                    $fieldData['parent'] = $this->getRelationModel($relationField['entity'], -1);
                }

                $fieldData['values'][$attributeKey] = $data[$attributeKey];

                array_set($relationData, 'relations.'.$key, $fieldData);
            }
        }

        return $relationData;
    }
}
