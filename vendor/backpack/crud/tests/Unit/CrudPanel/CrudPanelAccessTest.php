<?php

namespace Backpack\CRUD\Tests\Unit\CrudPanel;

use Backpack\CRUD\app\Exceptions\AccessDeniedException;

class CrudPanelAccessTest extends BaseCrudPanelTest
{
    private $unknownPermission = 'unknownPermission';

    private $defaultAccessList = [];

    private $fullAccessList = [
        'list',
        'create',
        'update',
        'delete',
        'bulkDelete',
        'revisions',
        'reorder',
        'show',
        'clone',
        'bulkClone',
    ];

    public function testHasAccess()
    {
        $this->crudPanel->allowAccess('list');
        $this->assertTrue($this->crudPanel->hasAccess('list'));
        $this->assertFalse($this->crudPanel->hasAccess('create'));
    }

    public function testAllowAccess()
    {
        $permission = 'reorder';

        $this->crudPanel->allowAccess($permission);

        $this->assertTrue($this->crudPanel->hasAccess($permission));
    }

    public function testAllowAccessToUnknownPermission()
    {
        $this->crudPanel->allowAccess($this->unknownPermission);

        $this->assertTrue($this->crudPanel->hasAccess($this->unknownPermission));
    }

    public function testDenyAccess()
    {
        $this->crudPanel->denyAccess('delete');

        $this->assertFalse($this->crudPanel->hasAccess('delete'));
    }

    public function testDenyAccessToUnknownPermission()
    {
        $this->crudPanel->denyAccess($this->unknownPermission);

        $this->assertFalse($this->crudPanel->hasAccess($this->unknownPermission));
    }

    public function testHasAccessToAny()
    {
        $this->crudPanel->allowAccess('create');

        $this->assertTrue($this->crudPanel->hasAccessToAny($this->fullAccessList));
    }

    public function testHasAccessToAnyDenied()
    {
        $this->assertFalse($this->crudPanel->hasAccessToAny(array_diff($this->fullAccessList, $this->defaultAccessList)));
    }

    public function testHasAccessToAll()
    {
        $this->crudPanel->allowAccess($this->fullAccessList);
        $this->assertTrue($this->crudPanel->hasAccessToAll($this->fullAccessList));
    }

    public function testHasAccessToAllDenied()
    {
        $this->assertFalse($this->crudPanel->hasAccessToAll($this->fullAccessList));
    }

    public function testHasAccessOrFail()
    {
        $this->crudPanel->allowAccess($this->fullAccessList);

        foreach ($this->fullAccessList as $permission) {
            $this->assertTrue($this->crudPanel->hasAccessOrFail($permission));
        }
    }

    public function testHasAccessOrFailDenied()
    {
        $this->expectException(AccessDeniedException::class);

        $this->crudPanel->hasAccessOrFail($this->unknownPermission);
    }
}
