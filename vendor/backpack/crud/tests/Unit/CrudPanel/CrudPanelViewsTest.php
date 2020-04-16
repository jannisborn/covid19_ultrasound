<?php

namespace Backpack\CRUD\Tests\Unit\CrudPanel;

use Config;

class CrudPanelViewsTest extends BaseCrudPanelTest
{
    private $customView = 'path/to/custom/view';
    private $customContentClass = 'col-md-12';

    // CREATE

    public function testSetCreateView()
    {
        $this->crudPanel->setCreateView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->get('create.view'));
    }

    public function testGetCreateView()
    {
        $this->crudPanel->setCreateView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->getCreateView());
    }

    public function testSetCreateContentClass()
    {
        $this->crudPanel->setCreateContentClass($this->customContentClass);
        $this->assertEquals($this->customContentClass, $this->crudPanel->get('create.contentClass'));
    }

    public function testGetCreateContentClass()
    {
        $this->crudPanel->setCreateContentClass($this->customContentClass);
        $this->assertEquals($this->customContentClass, $this->crudPanel->getCreateContentClass());
    }

    public function testGetCreateContentClassFromConfig()
    {
        Config::set('backpack.crud.operations.create.contentClass', $this->customContentClass);

        $this->assertEquals(Config::get('backpack.crud.operations.create.contentClass'), $this->crudPanel->getCreateContentClass());
    }

    // UPDATE

    public function testSetEditView()
    {
        $this->crudPanel->setEditView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->get('update.view'));
    }

    public function testGetEditView()
    {
        $this->crudPanel->setEditView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->getEditView());
    }

    public function testSetEditContentClass()
    {
        $this->crudPanel->setEditContentClass($this->customContentClass);
        $this->assertEquals($this->customContentClass, $this->crudPanel->get('update.contentClass'));
    }

    public function testGetEditContentClass()
    {
        $this->crudPanel->setEditContentClass($this->customContentClass);
        $this->assertEquals($this->customContentClass, $this->crudPanel->getEditContentClass());
    }

    public function testGetEditContentClassFromConfig()
    {
        Config::set('backpack.crud.operations.update.contentClass', $this->customContentClass);

        $this->assertEquals(Config::get('backpack.crud.operations.update.contentClass'), $this->crudPanel->getEditContentClass());
    }

    public function testSetUpdateView()
    {
        $this->crudPanel->setUpdateView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->get('update.view'));
    }

    public function testGetUpdateView()
    {
        $this->crudPanel->setEditView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->getUpdateView());
    }

    public function testSetUpdateContentClass()
    {
        $this->crudPanel->setUpdateContentClass($this->customContentClass);
        $this->assertEquals($this->customContentClass, $this->crudPanel->get('update.contentClass'));
    }

    public function testGetUpdateContentClass()
    {
        $this->crudPanel->setEditContentClass($this->customContentClass);
        $this->assertEquals($this->customContentClass, $this->crudPanel->getUpdateContentClass());
    }

    public function testGetUpdateContentClassFromConfig()
    {
        Config::set('backpack.crud.operations.update.contentClass', $this->customContentClass);

        $this->assertEquals(Config::get('backpack.crud.operations.update.contentClass'), $this->crudPanel->getUpdateContentClass());
    }

    // SHOW

    public function testSetShowView()
    {
        $this->crudPanel->setShowView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->get('show.view'));
    }

    public function testGetShowView()
    {
        $this->crudPanel->setShowView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->getShowView());
    }

    public function testSetShowContentClass()
    {
        $this->crudPanel->setShowContentClass($this->customContentClass);
        $this->assertEquals($this->customContentClass, $this->crudPanel->get('show.contentClass'));
    }

    public function testGetShowContentClass()
    {
        $this->crudPanel->setShowContentClass($this->customContentClass);
        $this->assertEquals($this->customContentClass, $this->crudPanel->getShowContentClass());
    }

    public function testGetShowContentClassFromConfig()
    {
        Config::set('backpack.crud.operations.show.contentClass', $this->customContentClass);

        $this->assertEquals(Config::get('backpack.crud.operations.show.contentClass'), $this->crudPanel->getShowContentClass());
    }

    public function testSetPreviewView()
    {
        $this->crudPanel->setPreviewView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->get('show.view'));
    }

    public function testGetPreviewView()
    {
        $this->crudPanel->setShowView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->getPreviewView());
    }

    // LIST ENTRIES

    public function testSetListView()
    {
        $this->crudPanel->setListView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->get('list.view'));
    }

    public function testGetListView()
    {
        $this->crudPanel->setListView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->getListView());
    }

    public function testSetListContentClass()
    {
        $this->crudPanel->setListContentClass($this->customContentClass);
        $this->assertEquals($this->customContentClass, $this->crudPanel->get('list.contentClass'));
    }

    public function testGetListContentClass()
    {
        $this->crudPanel->setListContentClass($this->customContentClass);
        $this->assertEquals($this->customContentClass, $this->crudPanel->getListContentClass());
    }

    public function testGetListContentClassFromConfig()
    {
        Config::set('backpack.crud.operations.list.contentClass', $this->customContentClass);

        $this->assertEquals(Config::get('backpack.crud.operations.list.contentClass'), $this->crudPanel->getListContentClass());
    }

    // DETAILS ROW

    public function testSetDetailsRowView()
    {
        $this->crudPanel->setDetailsRowView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->get('list.detailsRow.view'));
    }

    public function testGetDetailsRowView()
    {
        $this->crudPanel->setDetailsRowView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->getDetailsRowView());
    }

    // REORDER

    public function testSetReorderView()
    {
        $this->crudPanel->setReorderView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->get('reorder.view'));
    }

    public function testGetReorderView()
    {
        $this->crudPanel->setReorderView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->getReorderView());
    }

    public function testSetReorderContentClass()
    {
        $this->crudPanel->setReorderContentClass($this->customContentClass);
        $this->assertEquals($this->customContentClass, $this->crudPanel->get('reorder.contentClass'));
    }

    public function testGetReorderContentClass()
    {
        $this->crudPanel->setReorderContentClass($this->customContentClass);
        $this->assertEquals($this->customContentClass, $this->crudPanel->getReorderContentClass());
    }

    public function testGetReorderContentClassFromConfig()
    {
        Config::set('backpack.crud.operations.reorder.contentClass', $this->customContentClass);

        $this->assertEquals(Config::get('backpack.crud.operations.reorder.contentClass'), $this->crudPanel->getReorderContentClass());
    }

    // REVISIONS

    public function testSetRevisionsView()
    {
        $this->crudPanel->setRevisionsView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->get('revisions.view'));
    }

    public function testGetRevisionsView()
    {
        $this->crudPanel->setRevisionsView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->getRevisionsView());
    }

    public function testSetRevisionsTimelineView()
    {
        $this->crudPanel->setRevisionsTimelineView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->get('revisions.timelineView'));
    }

    public function testGetRevisionsTimelineView()
    {
        $this->crudPanel->setRevisionsTimelineView($this->customView);
        $this->assertEquals($this->customView, $this->crudPanel->getRevisionsTimelineView());
    }

    public function testSetRevisionsTimelineContentClass()
    {
        $this->crudPanel->setRevisionsTimelineContentClass($this->customContentClass);
        $this->assertEquals($this->customContentClass, $this->crudPanel->get('revisions.timelineContentClass'));
    }

    public function testGetRevisionsTimelineContentClass()
    {
        $this->crudPanel->setRevisionsTimelineContentClass($this->customContentClass);
        $this->assertEquals($this->customContentClass, $this->crudPanel->getRevisionsTimelineContentClass());
    }

    public function testGetRevisionsTimelineContentClassFromConfig()
    {
        Config::set('backpack.crud.operations.revisions.timelineContent', $this->customContentClass);

        $this->assertEquals(Config::get('backpack.crud.operations.revisions.timelineContent'), $this->crudPanel->getRevisionsTimelineContentClass());
    }
}
