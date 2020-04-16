<?php

namespace Backpack\CRUD\app\Library\CrudPanel\Traits;

use Backpack\CRUD\app\Exceptions\AccessDeniedException;

trait Access
{
    /**
     * Set an operation as having access using the Settings API.
     *
     * @param string $operation
     *
     * @return bool
     */
    public function allowAccess($operation)
    {
        foreach ((array) $operation as $op) {
            $this->set($op.'.access', true);
        }

        return $this->hasAccessToAll($operation);
    }

    /**
     * Disable the access to a certain operation, or the current one.
     *
     * @param bool $operation [description]
     *
     * @return [type] [description]
     */
    public function denyAccess($operation)
    {
        foreach ((array) $operation as $op) {
            $this->set($op.'.access', false);
        }

        return ! $this->hasAccessToAny($operation);
    }

    /**
     * Check if a operation is allowed for a Crud Panel. Return false if not.
     *
     * @param string $operation
     *
     * @return bool
     */
    public function hasAccess($operation)
    {
        return $this->get($operation.'.access') ?? false;
    }

    /**
     * Check if any operations are allowed for a Crud Panel. Return false if not.
     *
     * @param array $operation_array
     *
     * @return bool
     */
    public function hasAccessToAny($operation_array)
    {
        foreach ((array) $operation_array as $key => $operation) {
            if ($this->get($operation.'.access') == true) {
                return true;
            }
        }

        return false;
    }

    /**
     * Check if all operations are allowed for a Crud Panel. Return false if not.
     *
     * @param array $operation_array Permissions.
     *
     * @return bool
     */
    public function hasAccessToAll($operation_array)
    {
        foreach ((array) $operation_array as $key => $operation) {
            if (! $this->get($operation.'.access')) {
                return false;
            }
        }

        return true;
    }

    /**
     * Check if a operation is allowed for a Crud Panel. Fail if not.
     *
     * @param string $operation
     *
     * @throws \Backpack\CRUD\Exception\AccessDeniedException in case the operation is not enabled
     *
     * @return bool
     */
    public function hasAccessOrFail($operation)
    {
        if (! $this->get($operation.'.access')) {
            throw new AccessDeniedException(trans('backpack::crud.unauthorized_access', ['access' => $operation]));
        }

        return true;
    }
}
