export type NavigationBarConfig = {
  items: {
    name: string
    label: string
    icon: string
    activeIcon: string
  }[]
}

export type IconSize = 'small' | 'normal' | 'large'

export type IconItemConfig = {
  size: {
    [size in IconSize]: string
  }
}

export type Treatment = {
  id: string
  animalId: string
  name: string
  zone: string
  freq: number
}

export type MedicalAppointment = {
  id: string
  date: Date
  reason: string
}

export type Animal = {
  id: string
  name: string
  personality: string
  description: string
  sex: 'male' | 'female'
  birthDate: Date
  entryDate: Date
  yard: string
  isAnimalCompatible: boolean
  isCastrated: boolean
  treatmentList: string[]
  appointmentList: string[]
  hasTreatment?: boolean
  image?: string
}

export type TextFilter = {
  type: 'text'
  item: string
}

export type ContentFilter = {
  type: 'content'
  item: any[]
}

export type Filters = Record<string, TextFilter | ContentFilter>

export type User = {
  name: string
  surnames: string
  email: string
  isVeteran: boolean
  avatar?: string
}

export type AnimalFilters = {
  name: string
  yards: { [yard: string]: boolean }
  sex: { [sex: string]: boolean }
  age: {
    min: number
    max: number
  }
  castration: { [castration: string]: boolean }
  compatible: { [compatible: string]: boolean }
}
