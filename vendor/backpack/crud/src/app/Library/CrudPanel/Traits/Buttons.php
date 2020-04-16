<?php

namespace Backpack\CRUD\app\Library\CrudPanel\Traits;

use Illuminate\Support\Collection;

trait Buttons
{
    // ------------
    // BUTTONS
    // ------------

    /**
     * Order the CRUD buttons. If certain button names are missing from the given order array
     * they will be pushed to the end of the button collection.
     *
     *
     * @param string      $stack           Stack where the buttons belongs. Options: top, line, bottom.
     * @param array       $order           Ordered name of the buttons. ['update', 'delete', 'show']
     */
    public function orderButtons(string $stack, array $order)
    {
        $newButtons = collect([]);
        $otherButtons = collect([]);

        // we get the buttons that belong to the specified stack
        $stackButtons = $this->buttons()->reject(function ($item) use ($stack, $otherButtons) {
            if ($item->stack != $stack) {
                // if the button does not belong to this stack we just add it for merging later
                $otherButtons->push($item);

                return true;
            }

            return false;
        });

        // we parse the ordered buttons
        collect($order)->each(function ($btnKey) use ($newButtons, $stackButtons) {
            if (! $button = $stackButtons->where('name', $btnKey)->first()) {
                abort(500, 'Button name [«'.$btnKey.'»] not found.');
            }
            $newButtons->push($button);
        });

        // if the ordered buttons are less than the total number of buttons in the stack
        // we add the remaining buttons to the end of the ordered ones
        if (count($newButtons) < count($stackButtons)) {
            foreach ($stackButtons as $button) {
                if (! $newButtons->where('name', $button->name)->first()) {
                    $newButtons->push($button);
                }
            }
        }

        $this->setOperationSetting('buttons', $newButtons->merge($otherButtons));
    }

    /**
     * Add a button to the CRUD table view.
     *
     * @param string      $stack           Where should the button be visible? Options: top, line, bottom.
     * @param string      $name            The name of the button. Unique.
     * @param string      $type            Type of button: view or model_function.
     * @param string      $content         The HTML for the button.
     * @param bool|string $position        Position on the stack: beginning or end. If false, the position will be
     *                                     'beginning' for the line stack or 'end' otherwise.
     * @param bool        $replaceExisting True if a button with the same name on the given stack should be replaced.
     *
     * @return \Backpack\CRUD\app\Library\CrudPanel\Traits\CrudButton The new CRUD button.
     */
    public function addButton($stack, $name, $type, $content, $position = false, $replaceExisting = true)
    {
        if ($position == false) {
            switch ($stack) {
                case 'line':
                    $position = 'beginning';
                    break;

                default:
                    $position = 'end';
                    break;
            }
        }

        if ($replaceExisting) {
            $this->removeButton($name, $stack);
        }

        $button = new CrudButton($stack, $name, $type, $content);
        switch ($position) {
            case 'beginning':
                $this->setOperationSetting('buttons', $this->buttons()->prepend($button));
                break;

            default:
                $this->setOperationSetting('buttons', $this->buttons()->push($button));
                break;
        }

        return $button;
    }

    public function addButtonFromModelFunction($stack, $name, $model_function_name, $position = false)
    {
        $this->addButton($stack, $name, 'model_function', $model_function_name, $position);
    }

    public function addButtonFromView($stack, $name, $view, $position = false)
    {
        $view = 'crud::buttons.'.$view;

        $this->addButton($stack, $name, 'view', $view, $position);
    }

    /**
     * @return Collection
     */
    public function buttons()
    {
        return $this->getOperationSetting('buttons') ?? collect();
    }

    /**
     * Modify the attributes of a button.
     *
     * @param string $name          The button name.
     * @param array  $modifications The attributes and their new values.
     *
     * @return CrudButton The button that has suffered the changes, for daisychaining methods.
     */
    public function modifyButton($name, $modifications = null)
    {
        /**
         * @var CrudButton|null
         */
        $button = $this->buttons()->firstWhere('name', $name);

        if (! $button) {
            abort(500, 'CRUD Button "'.$name.'" not found. Please check the button exists before you modify it.');
        }

        if (is_array($modifications)) {
            foreach ($modifications as $key => $value) {
                $button->{$key} = $value;
            }
        }

        return $button;
    }

    /**
     * Remove a button from the CRUD panel.
     *
     * @param string $name  Button name.
     * @param string $stack Optional stack name.
     */
    public function removeButton($name, $stack = null)
    {
        $this->setOperationSetting('buttons', $this->buttons()->reject(function ($button) use ($name, $stack) {
            return $stack == null ? $button->name == $name : ($button->stack == $stack) && ($button->name == $name);
        }));
    }

    /**
     * @param array       $names Button names
     * @param string|null $stack Optional stack name.
     */
    public function removeButtons($names, $stack = null)
    {
        if (! empty($names)) {
            foreach ($names as $name) {
                $this->removeButton($name, $stack);
            }
        }
    }

    public function removeAllButtons()
    {
        $this->setOperationSetting('buttons', collect());
    }

    public function removeAllButtonsFromStack($stack)
    {
        $this->setOperationSetting('buttons', $this->buttons()->reject(function ($button) use ($stack) {
            return $button->stack == $stack;
        }));
    }

    public function removeButtonFromStack($name, $stack)
    {
        $this->setOperationSetting('buttons', $this->buttons()->reject(function ($button) use ($name, $stack) {
            return $button->name == $name && $button->stack == $stack;
        }));
    }
}

class CrudButton
{
    public $stack;
    public $name;
    public $type = 'view';
    public $content;

    public function __construct($stack, $name, $type, $content)
    {
        $this->stack = $stack;
        $this->name = $name;
        $this->type = $type;
        $this->content = $content;
    }
}
