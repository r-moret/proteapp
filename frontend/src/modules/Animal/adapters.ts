import { AnimalSchema } from './declarations'

export const AnimalAdapter = (input: any) => {
  return AnimalSchema.parse({
    ...input,
    birthDate: input.birth_date,
    entryDate: input.entry_date,
    isAnimalCompatible: input.is_animal_compatible,
    isCastrated: input.is_castrated
  })
}
