<?php

namespace Backpack\CRUD\app\Library\CrudPanel\Traits;

trait SaveActions
{
    /**
     * Get the developer's preference on what save action is the default one
     * for the current operation.
     *
     * @return string
     */
    public function getSaveActionDefaultForCurrentOperation()
    {
        return config('backpack.crud.operations.'.$this->getCurrentOperation().'.defaultSaveAction', 'save_and_back');
    }

    /**
     * Get save actions, with pre-selected action from stored session variable or config fallback.
     *
     * @return array
     */
    public function getSaveAction()
    {
        $saveAction = session($this->getCurrentOperation().'.saveAction', $this->getSaveActionDefaultForCurrentOperation());

        // Permissions and their related actions.
        $permissions = [
            'list'   => 'save_and_back',
            'update' => 'save_and_edit',
            'create' => 'save_and_new',
        ];

        $saveOptions = collect($permissions)
            // Restrict list to allowed actions.
            ->filter(function ($action, $permission) {
                return $this->hasAccess($permission);
            })
            // Generate list of possible actions.
            ->mapWithKeys(function ($action, $permission) {
                return [$action => $this->getSaveActionButtonName($action)];
            })
            ->all();

        // Set current action if it exist, or first available option.
        if (isset($saveOptions[$saveAction])) {
            $saveCurrent = [
                'value' => $saveAction,
                'label' => $saveOptions[$saveAction],
            ];
        } else {
            $saveCurrent = [
                'value' => key($saveOptions),
                'label' => reset($saveOptions),
            ];
        }

        // Remove active action from options.
        unset($saveOptions[$saveCurrent['value']]);

        return [
            'active'  => $saveCurrent,
            'options' => $saveOptions,
        ];
    }

    /**
     * Change the session variable that remembers what to do after the "Save" action.
     *
     * @param string|null $forceSaveAction
     *
     * @return void
     */
    public function setSaveAction($forceSaveAction = null)
    {
        $saveAction = $forceSaveAction ?:
            \Request::input('save_action', $this->getSaveActionDefaultForCurrentOperation());

        $showBubble = $this->getOperationSetting('showSaveActionChange') ?? config('backpack.crud.operations.'.$this->getCurrentOperation().'.showSaveActionChange') ?? true;

        if ($showBubble &&
            session($this->getCurrentOperation().'.saveAction', 'save_and_back') !== $saveAction) {
            \Alert::info(trans('backpack::crud.save_action_changed_notification'))->flash();
        }

        session([$this->getCurrentOperation().'.saveAction' => $saveAction]);
    }

    /**
     * Redirect to the correct URL, depending on which save action has been selected.
     *
     * @param string $itemId
     *
     * @return \Illuminate\Http\Response
     */
    public function performSaveAction($itemId = null)
    {
        $saveAction = \Request::input('save_action', $this->getSaveActionDefaultForCurrentOperation());
        $itemId = $itemId ?: \Request::input('id');

        switch ($saveAction) {
            case 'save_and_new':
                $redirectUrl = $this->route.'/create';
                break;
            case 'save_and_edit':
                $redirectUrl = $this->route.'/'.$itemId.'/edit';
                if (\Request::has('locale')) {
                    $redirectUrl .= '?locale='.\Request::input('locale');
                }
                if (\Request::has('current_tab')) {
                    $redirectUrl = $redirectUrl.'#'.\Request::get('current_tab');
                }
                break;
            case 'save_and_back':
            default:
                $redirectUrl = \Request::has('http_referrer') ? \Request::get('http_referrer') : $this->route;
                break;
        }

        // if the request is AJAX, return a JSON response
        if ($this->request->ajax()) {
            return [
                'success'      => true,
                'data'         => $this->entry,
                'redirect_url' => $redirectUrl,
            ];
        }

        return \Redirect::to($redirectUrl);
    }

    /**
     * Get the translated text for the Save button.
     *
     * @param string $actionValue
     *
     * @return string
     */
    private function getSaveActionButtonName($actionValue = 'save_and_back')
    {
        switch ($actionValue) {
            case 'save_and_edit':
                return trans('backpack::crud.save_action_save_and_edit');
                break;
            case 'save_and_new':
                return trans('backpack::crud.save_action_save_and_new');
                break;
            case 'save_and_back':
            default:
                return trans('backpack::crud.save_action_save_and_back');
                break;
        }
    }
}
