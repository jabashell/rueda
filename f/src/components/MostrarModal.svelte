<!-- ConfirmDialog.svelte -->
<script>
  import { Dialog, Button } from 'svelte-ux';

  export let open = false;          // Controla si el diálogo está abierto o cerrado
  export let onClose = () => {};    // Callback para cerrar el diálogo

  export let dialogTitle = "Are you sure?";
  export let dialogContent =
    "This will permanently delete the item and cannot be undone.";
  export let persistent=false;
</script>

<!-- Dialog controlado externamente -->
<Dialog {open} on:close={onClose} {persistent}>
  <div slot="title">{dialogTitle}</div>
  <div class="px-6 py-3 text-xl">
    {dialogContent}
  </div>
  <div slot="actions">
    <Button on:click={onClose}>Cancel</Button>
  </div>
</Dialog>



<style>

</style>