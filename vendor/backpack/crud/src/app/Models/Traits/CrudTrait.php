<?php

namespace Backpack\CRUD\app\Models\Traits;

use DB;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Config;
use Traversable;

trait CrudTrait
{
    public static function hasCrudTrait()
    {
        return true;
    }

    /*
    |--------------------------------------------------------------------------
    | Methods for ENUM and SELECT crud fields.
    |--------------------------------------------------------------------------
    */

    public static function getPossibleEnumValues($field_name)
    {
        $default_connection = Config::get('database.default');
        $table_prefix = Config::get('database.connections.'.$default_connection.'.prefix');

        $instance = new static(); // create an instance of the model to be able to get the table name
        $connectionName = $instance->getConnectionName();
        $type = DB::connection($connectionName)->select(DB::raw('SHOW COLUMNS FROM `'.$table_prefix.$instance->getTable().'` WHERE Field = "'.$field_name.'"'))[0]->Type;
        preg_match('/^enum\((.*)\)$/', $type, $matches);
        $enum = [];
        foreach (explode(',', $matches[1]) as $value) {
            $enum[] = trim($value, "'");
        }

        return $enum;
    }

    public static function getEnumValuesAsAssociativeArray($field_name)
    {
        $instance = new static();
        $enum_values = $instance->getPossibleEnumValues($field_name);

        $array = array_flip($enum_values);

        foreach ($array as $key => $value) {
            $array[$key] = $key;
        }

        return $array;
    }

    public static function isColumnNullable($column_name)
    {
        // create an instance of the model to be able to get the table name
        $instance = new static();

        $conn = DB::connection($instance->getConnectionName());
        $table = Config::get('database.connections.'.Config::get('database.default').'.prefix').$instance->getTable();

        // MongoDB columns are alway nullable
        if ($conn->getConfig()['driver'] === 'mongodb') {
            return true;
        }

        // register the enum, json and jsonb column type, because Doctrine doesn't support it
        $conn->getDoctrineSchemaManager()->getDatabasePlatform()->registerDoctrineTypeMapping('enum', 'string');
        $conn->getDoctrineSchemaManager()->getDatabasePlatform()->registerDoctrineTypeMapping('json', 'json_array');
        $conn->getDoctrineSchemaManager()->getDatabasePlatform()->registerDoctrineTypeMapping('jsonb', 'json_array');
        try {
            //check if column exists in database
            $conn->getDoctrineColumn($table, $column_name);

            return ! $conn->getDoctrineColumn($table, $column_name)->getNotnull();
        } catch (\Exception $e) {
            return true;
        }
    }

    /*
    |--------------------------------------------------------------------------
    | Methods for Fake Fields functionality (used in PageManager).
    |--------------------------------------------------------------------------
    */

    /**
     * Add fake fields as regular attributes, even though they are stored as JSON.
     *
     * @param array $columns - the database columns that contain the JSONs
     */
    public function addFakes($columns = ['extras'])
    {
        foreach ($columns as $key => $column) {
            if (! isset($this->attributes[$column])) {
                continue;
            }

            $column_contents = $this->{$column};

            if ($this->shouldDecodeFake($column)) {
                $column_contents = json_decode($column_contents);
            }

            if ((is_array($column_contents) || is_object($column_contents) || $column_contents instanceof Traversable)) {
                foreach ($column_contents as $fake_field_name => $fake_field_value) {
                    $this->setAttribute($fake_field_name, $fake_field_value);
                }
            }
        }
    }

    /**
     * Return the entity with fake fields as attributes.
     *
     * @param array $columns - the database columns that contain the JSONs
     *
     * @return Model
     */
    public function withFakes($columns = [])
    {
        $model = '\\'.get_class($this);

        $columnCount = ((is_array($columns) || $columns instanceof Countable) ? count($columns) : 0);

        if ($columnCount == 0) {
            $columns = (property_exists($model, 'fakeColumns')) ? $this->fakeColumns : ['extras'];
        }

        $this->addFakes($columns);

        return $this;
    }

    /**
     * Determine if this fake column should be json_decoded.
     *
     * @param $column string fake column name
     *
     * @return bool
     */
    public function shouldDecodeFake($column)
    {
        return ! in_array($column, array_keys($this->casts));
    }

    /**
     * Determine if this fake column should get json_encoded or not.
     *
     * @param $column string fake column name
     *
     * @return bool
     */
    public function shouldEncodeFake($column)
    {
        return ! in_array($column, array_keys($this->casts));
    }

    /*
    |--------------------------------------------------------------------------
    | Methods for storing uploaded files (used in CRUD).
    |--------------------------------------------------------------------------
    */

    /**
     * Handle file upload and DB storage for a file:
     * - on CREATE
     *     - stores the file at the destination path
     *     - generates a name
     *     - stores the full path in the DB;
     * - on UPDATE
     *     - if the value is null, deletes the file and sets null in the DB
     *     - if the value is different, stores the different file and updates DB value.
     *
     * @param string $value            Value for that column sent from the input.
     * @param string $attribute_name   Model attribute name (and column in the db).
     * @param string $disk             Filesystem disk used to store files.
     * @param string $destination_path Path in disk where to store the files.
     */
    public function uploadFileToDisk($value, $attribute_name, $disk, $destination_path)
    {
        // if a new file is uploaded, delete the file from the disk
        if (request()->hasFile($attribute_name) &&
            $this->{$attribute_name} &&
            $this->{$attribute_name} != null) {
            \Storage::disk($disk)->delete($this->{$attribute_name});
            $this->attributes[$attribute_name] = null;
        }

        // if the file input is empty, delete the file from the disk
        if (is_null($value) && $this->{$attribute_name} != null) {
            \Storage::disk($disk)->delete($this->{$attribute_name});
            $this->attributes[$attribute_name] = null;
        }

        // if a new file is uploaded, store it on disk and its filename in the database
        if (request()->hasFile($attribute_name) && request()->file($attribute_name)->isValid()) {
            // 1. Generate a new file name
            $file = request()->file($attribute_name);
            $new_file_name = md5($file->getClientOriginalName().random_int(1, 9999).time()).'.'.$file->getClientOriginalExtension();

            // 2. Move the new file to the correct path
            $file_path = $file->storeAs($destination_path, $new_file_name, $disk);

            // 3. Save the complete path to the database
            $this->attributes[$attribute_name] = $file_path;
        }
    }

    /**
     * Handle multiple file upload and DB storage:
     * - if files are sent
     *     - stores the files at the destination path
     *     - generates random names
     *     - stores the full path in the DB, as JSON array;
     * - if a hidden input is sent to clear one or more files
     *     - deletes the file
     *     - removes that file from the DB.
     *
     * @param string $value            Value for that column sent from the input.
     * @param string $attribute_name   Model attribute name (and column in the db).
     * @param string $disk             Filesystem disk used to store files.
     * @param string $destination_path Path in disk where to store the files.
     */
    public function uploadMultipleFilesToDisk($value, $attribute_name, $disk, $destination_path)
    {
        if (! is_array($this->{$attribute_name})) {
            $attribute_value = json_decode($this->{$attribute_name}, true) ?? [];
        } else {
            $attribute_value = $this->{$attribute_name};
        }
        $files_to_clear = request()->get('clear_'.$attribute_name);

        // if a file has been marked for removal,
        // delete it from the disk and from the db
        if ($files_to_clear) {
            foreach ($files_to_clear as $key => $filename) {
                \Storage::disk($disk)->delete($filename);
                $attribute_value = array_where($attribute_value, function ($value, $key) use ($filename) {
                    return $value != $filename;
                });
            }
        }

        // if a new file is uploaded, store it on disk and its filename in the database
        if (request()->hasFile($attribute_name)) {
            foreach (request()->file($attribute_name) as $file) {
                if ($file->isValid()) {
                    // 1. Generate a new file name
                    $new_file_name = md5($file->getClientOriginalName().random_int(1, 9999).time()).'.'.$file->getClientOriginalExtension();

                    // 2. Move the new file to the correct path
                    $file_path = $file->storeAs($destination_path, $new_file_name, $disk);

                    // 3. Add the public path to the database
                    $attribute_value[] = $file_path;
                }
            }
        }

        $this->attributes[$attribute_name] = json_encode($attribute_value);
    }

    /*
    |--------------------------------------------------------------------------
    | Methods for working with translatable models.
    |--------------------------------------------------------------------------
    */

    /**
     * Get the attributes that were casted in the model.
     * Used for translations because Spatie/Laravel-Translatable
     * overwrites the getCasts() method.
     *
     * @return self
     */
    public function getCastedAttributes()
    {
        return parent::getCasts();
    }

    /**
     * Check if a model is translatable.
     * All translation adaptors must have the translationEnabledForModel() method.
     *
     * @return bool
     */
    public function translationEnabled()
    {
        if (method_exists($this, 'translationEnabledForModel')) {
            return $this->translationEnabledForModel();
        }

        return false;
    }
}
