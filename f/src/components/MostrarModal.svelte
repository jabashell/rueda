<script>
    export let fecha = '';
    export let conductor = "";
    export let grupo = '';

    import { Toggle, Button, Dialog } from "svelte-ux";
</script>


<Toggle let:on={open} let:toggle let:toggleOff>
    <Button on:click={toggle} color="danger">Delete</Button>
    <Dialog {open} on:close={toggleOff}>
      <div slot="title">Are you sure?</div>
      <div class="px-6 py-3">
        This will permanently delete the item and can not be undone.
      </div>
      <div slot="actions">
        <Button
          on:click={() => {
            console.log("Deleting item...");
          }}
          variant="fill"
          color="danger"
        >
          Yes, delete item
        </Button>
        <Button>Cancel</Button>
      </div>
    </Dialog>
  </Toggle>



<style>

</style>