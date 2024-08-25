<script setup lang="ts">
// const newUserPerson = ref<Person>()

// async function handleAddUser(closeDrawer: () => void) {
//   if (!newUser.value || !newUserPerson.value) return

//   try {
//     newUser.value.person = newUserPerson.value.id

//     EditUserAdapter(newUser.value)

//     await userStore.createUser(newUser.value)
//     showSuccessNotification('Usuario añadido correctamente.')

//     newUser.value = {
//       person: '',
//       image: null,
//       active: true,
//       veteran: false,
//       password: ''
//     }
//     newUserPerson.value = undefined
//     closeDrawer()
//   } catch (error) {
//     if (error instanceof ZodError) {
//       showErrorNotification('Parece que hay un error con los datos del usuario.')
//     } else {
//       showErrorNotification('Ha ocurrido un error, prueba otra vez.')
//     }
//   }
// }
</script>

<template>
  Editor
  <!-- <BottomDrawer class="bg-base-200" size="small" v-model="newUserOpen" v-slot="{ close }">
      <div class="flex h-full flex-col gap-5">
        <h1 class="text-3xl font-semibold">Nuevo usuario</h1>
        <div v-if="newUser" class="flex h-full flex-col gap-6 pb-10">
          <div class="flex flex-col gap-2">
            <section class="flex flex-col gap-2">
              <h2 class="text-xl font-semibold">Persona</h2>
              <PersonSelector v-model="newUserPerson" />
            </section>
            <section class="flex flex-col gap-2">
              <h2 class="text-xl font-semibold">Veterano</h2>
              <div class="flex items-center gap-3">
                <label class="text-lg font-medium" for="veteranToggle">
                  {{ newUser.veteran ? 'Sí' : 'No' }}
                </label>
                <input
                  type="checkbox"
                  id="veteranToggle"
                  v-model="newUser.veteran"
                  class="toggle bg-secondary"
                />
              </div>
            </section>
          </div>
          <button
            @click="handleAddUser(close)"
            class="w-fit self-center rounded-lg bg-secondary px-10 py-3 text-xl font-semibold text-white"
          >
            Añadir
          </button>
        </div>
      </div>
    </BottomDrawer> -->
</template>
