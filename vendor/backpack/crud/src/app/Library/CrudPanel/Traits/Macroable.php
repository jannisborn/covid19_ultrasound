<?php

namespace Backpack\CRUD\app\Library\CrudPanel\Traits;

use Illuminate\Support\Traits\Macroable as IlluminateMacroable;

trait Macroable
{
    use IlluminateMacroable {
        IlluminateMacroable::macro as parentMacro;
    }

    /**
     * In addition to registering the macro, throw an error if the method already exists on the object
     * so the developer knows why his macro is not being registered.
     *
     * @param string          $name
     * @param object|callable $macro
     *
     * @return void
     */
    public static function macro($name, $macro)
    {
        if (method_exists(new static(), $name)) {
            abort(500, "Cannot register '$name' macro. '$name()' already exists on ".get_called_class());
        }

        static::parentMacro($name, $macro);
    }
}
