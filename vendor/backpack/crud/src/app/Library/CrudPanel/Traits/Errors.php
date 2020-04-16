<?php

namespace Backpack\CRUD\app\Library\CrudPanel\Traits;

trait Errors
{
    // -------
    // Getters
    // -------

    /**
     * @return bool
     */
    public function groupedErrorsEnabled()
    {
        return $this->getOperationSetting('groupedErrors');
    }

    /**
     * @return bool
     */
    public function inlineErrorsEnabled()
    {
        return $this->getOperationSetting('inlineErrors');
    }

    // -------
    // Setters
    // -------

    public function enableGroupedErrors()
    {
        return $this->setOperationSetting('groupedErrors', true);
    }

    public function disableGroupedErrors()
    {
        return $this->setOperationSetting('groupedErrors', false);
    }

    public function enableInlineErrors()
    {
        return $this->setOperationSetting('inlineErrors', true);
    }

    public function disableInlineErrors()
    {
        return $this->setOperationSetting('inlineErrors', false);
    }
}
