<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

/**
 * App\ImageType
 *
 * @mixin \Eloquent
 * @property int $id
 * @property \Illuminate\Support\Carbon|null $created_at
 * @property \Illuminate\Support\Carbon|null $updated_at
 * @property string $name
 * @method static \Illuminate\Database\Eloquent\Builder|\App\ImageType newModelQuery()
 * @method static \Illuminate\Database\Eloquent\Builder|\App\ImageType newQuery()
 * @method static \Illuminate\Database\Eloquent\Builder|\App\ImageType query()
 * @method static \Illuminate\Database\Eloquent\Builder|\App\ImageType whereCreatedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\ImageType whereId($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\ImageType whereName($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\ImageType whereUpdatedAt($value)
 */
class ImageType extends Model
{
    protected $table = 'image_types';
}
