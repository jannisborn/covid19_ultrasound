<?php

namespace Backpack\CRUD\app\Library\CrudPanel\Traits;

use Venturecraft\Revisionable\Revision;

trait ViewsAndRestoresRevisions
{
    /**
     * Build a list of Revisions, grouped by revision date.
     *
     * @param int $id
     *
     * @return array array of revision groups, keyed by revision date
     */
    public function listRevisions($id)
    {
        $revisions = [];
        // Group revisions by change date
        foreach ($this->getEntry($id)->revisionHistory as $history) {
            // Get just the date from the revision created timestamp
            $revisionDate = date('Y-m-d', strtotime((string) $history->created_at));

            // Be sure to instantiate the initial grouping array
            if (! array_key_exists($revisionDate, $revisions)) {
                $revisions[$revisionDate] = [];
            }

            // Push onto the top of the current group - so we get orderBy decending timestamp
            array_unshift($revisions[$revisionDate], $history);
        }

        // Sort the array by timestamp descending (so that the most recent are at the top)
        krsort($revisions);

        return $revisions;
    }

    /**
     * Restore a single revision.
     *
     * @param int $id         The ID of the source CRUD Model instance to update
     * @param int $revisionId The ID of the revision to use for the update
     */
    public function restoreRevision($id, $revisionId)
    {
        $entry = $this->getEntryWithoutFakes($id);
        $revision = Revision::findOrFail($revisionId);

        // Update the revisioned field with the old value
        $entry->update([$revision->key => $revision->old_value]);

        // Reload the entry so we have the latest revisions
        $entry = $this->getEntry($id);
    }
}
