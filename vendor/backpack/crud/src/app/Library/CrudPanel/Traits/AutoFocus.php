<?php

namespace Backpack\CRUD\app\Library\CrudPanel\Traits;

trait AutoFocus
{
    /**
     * @return bool
     */
    public function getAutoFocusOnFirstField()
    {
        return $this->getOperationSetting('autoFocusOnFirstField');
    }

    public function setAutoFocusOnFirstField($value)
    {
        return $this->setOperationSetting('autoFocusOnFirstField', (bool) $value);
    }

    public function enableAutoFocus()
    {
        return $this->setAutoFocusOnFirstField(true);
    }

    public function disableAutoFocus()
    {
        return $this->setAutoFocusOnFirstField(false);
    }
}
