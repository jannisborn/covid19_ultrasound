<?php

namespace Backpack\CRUD\app\Library\CrudPanel;

use Illuminate\Support\Facades\Facade;

/**
 * This object allows developers to use CRUD::addField() instead of $this->crud->addField(),
 * by providing a Facade that leads to the CrudPanel object. That object is stored in Laravel's
 * service container as 'crud'.
 */
class CrudPanelFacade extends Facade
{
    /**
     * Get the registered name of the component.
     *
     * @return string
     */
    protected static function getFacadeAccessor()
    {
        return 'crud';
    }
}
