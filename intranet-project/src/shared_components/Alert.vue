<template>
    <div class="alert alert-warning alert-dismissible fade show" role="alert">
        <slot></slot>
        <button
            type="button"
            class="close"
            data-dismiss="alert"
            aria-label="Close"
        >
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
</template>

<style>
.alert {
    position: fixed;
    bottom: 0px;
}
</style>