<?php

namespace Backpack\CRUD\app\Library\CrudPanel\Traits;

trait Views
{
    // -------
    // CREATE
    // -------

    /**
     * Sets the create template.
     *
     * @param string $view name of the template file
     *
     * @return string $view name of the template file
     */
    public function setCreateView($view)
    {
        return $this->set('create.view', $view);
    }

    /**
     * Gets the create template.
     *
     * @return string name of the template file
     */
    public function getCreateView()
    {
        return $this->get('create.view') ?? 'crud::create';
    }

    /**
     * Sets the create content class.
     *
     * @param string $class content class
     */
    public function setCreateContentClass(string $class)
    {
        return $this->set('create.contentClass', $class);
    }

    /**
     * Gets the create content class.
     *
     * @return string content class for create view
     */
    public function getCreateContentClass()
    {
        return $this->get('create.contentClass') ?? config('backpack.crud.operations.create.contentClass', 'col-md-8 bold-labels');
    }

    // -------
    // READ
    // -------

    /**
     * Sets the list template.
     *
     * @param string $view name of the template file
     *
     * @return string $view name of the template file
     */
    public function setListView($view)
    {
        return $this->set('list.view', $view);
    }

    /**
     * Gets the list template.
     *
     * @return string name of the template file
     */
    public function getListView()
    {
        return $this->get('list.view') ?? 'crud::list';
    }

    /**
     * Sets the list content class.
     *
     * @param string $class content class
     */
    public function setListContentClass(string $class)
    {
        return $this->set('list.contentClass', $class);
    }

    /**
     * Gets the list content class.
     *
     * @return string content class for list view
     */
    public function getListContentClass()
    {
        return $this->get('list.contentClass') ?? config('backpack.crud.operations.list.contentClass', 'col-md-12');
    }

    /**
     * Sets the details row template.
     *
     * @param string $view name of the template file
     *
     * @return string $view name of the template file
     */
    public function setDetailsRowView($view)
    {
        return $this->set('list.detailsRow.view', $view);
    }

    /**
     * Gets the details row template.
     *
     * @return string name of the template file
     */
    public function getDetailsRowView()
    {
        return $this->get('list.detailsRow.view') ?? 'crud::details_row';
    }

    /**
     * Sets the show template.
     *
     * @param string $view name of the template file
     *
     * @return string $view name of the template file
     */
    public function setShowView($view)
    {
        return $this->set('show.view', $view);
    }

    /**
     * Gets the show template.
     *
     * @return string name of the template file
     */
    public function getShowView()
    {
        return $this->get('show.view') ?? 'crud::show';
    }

    /**
     * Sets the edit content class.
     *
     * @param string $class content class
     */
    public function setShowContentClass(string $class)
    {
        return $this->set('show.contentClass', $class);
    }

    /**
     * Gets the edit content class.
     *
     * @return string content class for edit view
     */
    public function getShowContentClass()
    {
        return $this->get('show.contentClass') ?? config('backpack.crud.operations.show.contentClass', 'col-md-8 col-md-offset-2');
    }

    // -------
    // UPDATE
    // -------

    /**
     * Sets the edit template.
     *
     * @param string $view name of the template file
     *
     * @return string $view name of the template file
     */
    public function setEditView($view)
    {
        return $this->set('update.view', $view);
    }

    /**
     * Gets the edit template.
     *
     * @return string name of the template file
     */
    public function getEditView()
    {
        return $this->get('update.view') ?? 'crud::edit';
    }

    /**
     * Sets the edit content class.
     *
     * @param string $class content class
     */
    public function setEditContentClass(string $class)
    {
        return $this->set('update.contentClass', $class);
    }

    /**
     * Gets the edit content class.
     *
     * @return string content class for edit view
     */
    public function getEditContentClass()
    {
        return $this->get('update.contentClass') ?? config('backpack.crud.operations.update.contentClass', 'col-md-8 bold-labels');
    }

    /**
     * Sets the reorder template.
     *
     * @param string $view name of the template file
     *
     * @return string $view name of the template file
     */
    public function setReorderView($view)
    {
        return $this->set('reorder.view', $view);
    }

    /**
     * Gets the reorder template.
     *
     * @return string name of the template file
     */
    public function getReorderView()
    {
        return $this->get('reorder.view') ?? 'crud::reorder';
    }

    /**
     * Sets the reorder content class.
     *
     * @param string $class content class
     */
    public function setReorderContentClass(string $class)
    {
        return $this->set('reorder.contentClass', $class);
    }

    /**
     * Gets the reorder&nest content class.
     *
     * @return string content class for reorder and nest view
     */
    public function getReorderContentClass()
    {
        return $this->get('reorder.contentClass') ?? config('backpack.crud.operations.reorder.contentClass', 'col-md-8 col-md-offset-2');
    }

    /**
     * Sets the revision template.
     *
     * @param string $view name of the template file
     *
     * @return string $view name of the template file
     */
    public function setRevisionsView($view)
    {
        return $this->set('revisions.view', $view);
    }

    /**
     * Sets the revision template.
     *
     * @param string $view name of the template file
     *
     * @return string $view name of the template file
     */
    public function setRevisionsTimelineView($view)
    {
        return $this->set('revisions.timelineView', $view);
    }

    /**
     * Gets the revisions template.
     *
     * @return string name of the template file
     */
    public function getRevisionsView()
    {
        return $this->get('revisions.view') ?? 'crud::revisions';
    }

    /**
     * Gets the revisions template.
     *
     * @return string name of the template file
     */
    public function getRevisionsTimelineView()
    {
        return $this->get('revisions.timelineView') ?? 'crud::inc.revision_timeline';
    }

    /**
     * Sets the revisions timeline content class.
     *
     * @param string revisions timeline content class
     */
    public function setRevisionsTimelineContentClass(string $class)
    {
        $this->set('revisions.timelineContentClass', $class);
    }

    /**
     * Gets the revisions timeline content class.
     *
     * @return string content class for revisions timeline view
     */
    public function getRevisionsTimelineContentClass()
    {
        return $this->get('revisions.timelineContentClass') ?? config('backpack.crud.operations.revisions.timelineContentClass', 'col-md-12');
    }

    // -------
    // ALIASES
    // -------

    public function getPreviewView()
    {
        return $this->getShowView();
    }

    public function setPreviewView($view)
    {
        return $this->setShowView($view);
    }

    public function getUpdateView()
    {
        return $this->getEditView();
    }

    public function setUpdateView($view)
    {
        return $this->setEditView($view);
    }

    public function setUpdateContentClass(string $editContentClass)
    {
        return $this->setEditContentClass($editContentClass);
    }

    public function getUpdateContentClass()
    {
        return $this->getEditContentClass();
    }
}
