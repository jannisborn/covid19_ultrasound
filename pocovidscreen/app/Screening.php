<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

/**
 * App\Screening
 *
 * @property int $id
 * @property \Illuminate\Support\Carbon|null $created_at
 * @property \Illuminate\Support\Carbon|null $updated_at
 * @property int $user_id
 * @property string $result
 * @property int $type_id
 * @property int file_id
 * @mixin \Eloquent
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Screening newModelQuery()
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Screening newQuery()
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Screening query()
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Screening whereCreatedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Screening whereId($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Screening whereResult($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Screening whereTypeId($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Screening whereUpdatedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Screening whereUserId($value)
 * @property-read \Illuminate\Database\Eloquent\Collection|\App\File[] $images
 * @property-read int|null $images_count
 * @method static \Illuminate\Database\Eloquent\Builder|\App\Screening whereFileId($value)
 */
class Screening extends Model
{
    protected $table = 'screenings';
    protected $fillable = ['user_id', 'result', 'type_id', 'file_id'];

    /**
     * @param $value
     * @return mixed
     */
    public function getResultAttribute($value) {
        return json_decode($value);
    }
}
