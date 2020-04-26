<?php

namespace App\Http\Controllers\Admin;

use App\Http\Requests\TrainingRequest;
use App\Models\Training;
use Backpack\CRUD\app\Http\Controllers\CrudController;
use Backpack\CRUD\app\Library\CrudPanel\CrudPanelFacade as CRUD;

/**
 * Class TrainingCrudController
 * @package App\Http\Controllers\Admin
 * @property-read \Backpack\CRUD\app\Library\CrudPanel\CrudPanel $crud
 */
class TrainingCrudController extends CrudController
{
    use \Backpack\CRUD\app\Http\Controllers\Operations\ListOperation;
    use \Backpack\CRUD\app\Http\Controllers\Operations\UpdateOperation;
    use \Backpack\CRUD\app\Http\Controllers\Operations\DeleteOperation;

    /**
     * @throws \Exception
     */
    public function setup()
    {
        $this->crud->setModel(Training::class);
        $this->crud->setRoute(config('backpack.base.route_prefix') . '/training');
        $this->crud->setEntityNameStrings('Training', 'Trainings');
    }

    protected function setupListOperation()
    {
        $this->crud->addColumn([
            'name' => 'created_at',
            'label' => "Creation date",
        ]);
        $this->crud->addColumn([
            'name' => 'file.path',
            'label' => "Image",
            'type' => 'Image',
            'disk' => 'local',
            'width' => '200px',
            'height' => '200px',
        ]);
    }

    protected function setupUpdateOperation()
    {

    }
}
