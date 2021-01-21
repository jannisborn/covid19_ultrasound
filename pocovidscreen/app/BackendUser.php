<?php

namespace App;

/**
 * App\BackendUser
 *
 * @property int $id
 * @property string $name
 * @property string $email
 * @property string|null $password
 * @property string|null $remember_token
 * @property \Illuminate\Support\Carbon|null $created_at
 * @property \Illuminate\Support\Carbon|null $updated_at
 * @property-read \Illuminate\Notifications\DatabaseNotificationCollection|\Illuminate\Notifications\DatabaseNotification[] $notifications
 * @property-read int|null $notifications_count
 * @method static \Illuminate\Database\Eloquent\Builder|\App\BackendUser newModelQuery()
 * @method static \Illuminate\Database\Eloquent\Builder|\App\BackendUser newQuery()
 * @method static \Illuminate\Database\Eloquent\Builder|\App\BackendUser query()
 * @method static \Illuminate\Database\Eloquent\Builder|\App\BackendUser whereCreatedAt($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\BackendUser whereEmail($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\BackendUser whereId($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\BackendUser whereName($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\BackendUser wherePassword($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\BackendUser whereRememberToken($value)
 * @method static \Illuminate\Database\Eloquent\Builder|\App\BackendUser whereUpdatedAt($value)
 * @mixin \Eloquent
 */
class BackendUser extends User
{
    protected $table = 'backend_users';
}
