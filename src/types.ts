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
