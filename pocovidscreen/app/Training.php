<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

/**
 * App\Training
 *
 * @property int $id
 * @property \Illuminate\Support\Carbon|null $created_at
 * @property \Illuminate\Support\Carbon|null $updated_at
 * @property int $user_id
 * @property int $type_id
 * @property int $pathology_id
 * @property int $file_id
 * @property-read mixed $result
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Training newModelQuery()
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Training newQuery()
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Training query()
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Training whereCreatedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Training whereFileId($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Training whereId($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Training wherePathologyId($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Training whereTypeId($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Training whereUpdatedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Training whereUserId($value)
 * @mixin \Eloquent
 */
class Training extends Model
{
    protected $table = 'trainings';
    protected $fillable = ['user_id', 'type_id', 'file_id', 'pathology_id'];

    /**
     * @return mixed
     */
    public function getResultAttribute($value) {
        return json_decode($value);
    }
}
